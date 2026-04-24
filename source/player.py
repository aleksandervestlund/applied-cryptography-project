from dataclasses import dataclass, field
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from socket import socket

from source.board import Board
from source.client import get_conn
from source.input_helpers import create_ships, get_role
from source.role import Role
from source.constants import HTML_FILE_PATH

def setup_browser() -> webdriver.Chrome:
    """Helper function to set up the headless browser."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Run in background
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3') # Suppress annoying Chrome terminal warnings
    return webdriver.Chrome(options=options)

@dataclass(slots=True)
class Player:
    board: Board = field(init=False)
    is_host: bool = field(init=False)
    conn: socket = field(init=False)
    
    # 1. Add the driver field. We set init=False so dataclass doesn't 
    # expect us to pass it when calling Player()
    driver: webdriver.Chrome = field(init=False) 

    def __post_init__(self) -> None:
        ships = create_ships()
        self.board = Board(ships)
        role = get_role()
        self.is_host = role is Role.HOST
        self.conn = get_conn(role)
        
        # 2. Boot up the browser instance for this specific player
        print("Starting local ZKP engine...")
        self.driver = setup_browser()

    # 3. Add a cleanup method
    def close(self) -> None:
        """Closes connections and kills the hidden browser process."""
        print("Cleaning up resources...")
        if self.conn:
            self.conn.close()
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()  # VERY IMPORTANT to avoid zombie processes
    
    def generate_proof(self, a: int, b: int) -> tuple[str, str]:
        """Generates a proof using the player's dedicated browser instance."""
        self.driver.get(HTML_FILE_PATH)
        print(self.driver.title)
        wait = WebDriverWait(self.driver, 10)
        
        # 1. Wait for inputs to load and enter the values
        input_a = wait.until(EC.presence_of_element_located((By.ID, "input_a")))
        input_b = self.driver.find_element(By.ID, "input_b")
        
        input_a.clear()
        input_a.send_keys(str(a))
        
        input_b.clear()
        input_b.send_keys(str(b))
        
        # 2. Click 'Generate Proof'
        proof_btn = self.driver.find_element(By.ID, "proofbutton")
        proof_btn.click()
        
        # 3. Wait until the button is re-enabled (this means proof generation is done)
        wait.until(EC.element_to_be_clickable((By.ID, "proofbutton")))
        
        # 4. Extract the proof and public signals as strings
        proof_data = self.driver.find_element(By.ID, "proofData").get_attribute("value")
        public_signals = self.driver.find_element(By.ID, "publicSignals").get_attribute("value")
        
        return proof_data, public_signals

    def verify_proof(self, proof_data: str, public_signals: str):
        """VERIFIER: Takes the generated proof/signals and verifies them."""
        self.driver.get(HTML_FILE_PATH)
        wait = WebDriverWait(self.driver, 10)
        
        # 1. Wait for the text areas to appear
        proof_textarea = wait.until(EC.presence_of_element_located((By.ID, "proofData")))
        signals_textarea = self.driver.find_element(By.ID, "publicSignals")
        
        # 2. Use JavaScript to quickly inject the large JSON strings
        self.driver.execute_script("arguments[0].value = arguments[1];", proof_textarea, proof_data)
        self.driver.execute_script("arguments[0].value = arguments[1];", signals_textarea, public_signals)
        
        # 3. Click 'Verify Proof'
        verify_btn = self.driver.find_element(By.ID, "verifybutton")
        verify_btn.click()
        
        # 4. Wait until the verify button is re-enabled (meaning checking is done)
        wait.until(EC.element_to_be_clickable((By.ID, "verifybutton")))
        
        # 5. Extract the result text (✅ Proof is valid / ❌ Proof is invalid)
        result_text = self.driver.find_element(By.ID, "result").text
        
        return "✅" in result_text
