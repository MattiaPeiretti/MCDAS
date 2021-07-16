import os

# Print iterations progress
def generateProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 25, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    iteration = abs(iteration)
    percent = ("{0:." + str(decimals) + "f}").format(abs(100 * (iteration / float(total))))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + ' ' * (length - filledLength)
    return f'{prefix} |{bar}| {percent}% {suffix}'
    # Print New Line on Complete
    if iteration == total: 
        print()

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

class GUI():
    def __init__(self, name, lat_margins=None, lon_margins=None):
        self.name = name
        self.lat_margins = lat_margins
        self.lon_margins = lon_margins

    def update(self, slon, lat, lon, current_value):
        lat_range = self.lat_margins[1] - self.lat_margins[0]
        
        lon_range = self.lon_margins[1] - self.lon_margins[0]

        slon_percentage = round(100*(abs(slon)/360), 2)

        lat_percentage = round(100*((lat - self.lat_margins[0])/lat_range), 2)
        
        lon_percentage = round(100*((lon - self.lon_margins[0])/lon_range), 2)
        screen = f"""
+===================================================+
                                                    
  {self.name}
                                                    
  Total work: {slon_percentage}%
   -> {generateProgressBar(slon, 360)}              
                                                    
  Latitude: {lat_percentage}%                       
   -> {generateProgressBar(lat - self.lat_margins[0], lat_range)}         
                                                    
  Longitude: {lon_percentage}%                      
   -> {generateProgressBar(lon - self.lon_margins[0], lon_range)}         
                                                    
  Current Solar Longitude: {slon}                   
  Current latitude: {lat} / { self.lat_margins[1]}  
  Current longitude: {lon} / { self.lon_margins[1]} 
  Current Value: {current_value}                    
                                                   
+===================================================+
        """
        
        cls()
        print(screen)

    def display_error(self, error_name, error):
        screen = f"""
+===================================================+
                                                    
  {error_name}

  {error}
                                                                                                                          
+===================================================+
        """
        
        cls()
        print(screen)