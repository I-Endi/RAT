

from io import TextIOWrapper


class Injector:
    """
    Injects any malicious code to a specified file
    """
    
    def __init__(self, target_file: TextIOWrapper, malware_file: TextIOWrapper) -> None:
        """
        Constructor
        
        :param target_file: The target file to inject the code to
        :param malware_file: .txt file with malicious code to inject
        """
        
        self.target_file = target_file
        self.malware_file = malware_file
    
    
    def malware_as_str(self) -> str:
        """
        Reads file with malware and extracts it to str
        
        :returns: Malicious code from malware_file.py
        """
        
        with open(self.malware_file, 'r') as file:
            malware_str = file.read()
        
        return malware_str
