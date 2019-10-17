# Expedia-Scraper
Python script to scrape flight information from Expedia using LXML and Selenium.

One-way trip query:
```
python ExpediaScraper.py <departure_city> <destination_city> <departure_date>
```

Round trip query:
```
python ExpediaScraper.py <departure_city> <destination_city> <departure_date> <return_date>
```

Example output:
One-way:
```Checking one-way flights from JFK to MNL on 06/05/2020
Departure   Arrival     Price       Duration   
8:55pm      1:05pm+2    $625        28h 10m    
8:55pm      3:35pm+2    $625        30h 40m    
8:55pm      5:25pm+2    $625        32h 30m    
8:55pm      11:00pm+2   $625        38h 5m     
1:35am      9:35am+1    $671        20h 0m    
```

Round trip:
```
Departure   Arrival     Price       Duration   
-> Return Flight Details
8:55pm      1:05pm+2    $883        28h 10m    
   2:15pm      11:10am+1   + $0        32h 55m    
   7:40am      11:10am+1   + $0        39h 30m    
   6:30pm      11:10am+1   + $47       28h 40m    
   4:40pm      11:10am+1   + $47       30h 30m    
   9:30pm      10:30pm+1   + $245      37h 0m     
8:55pm      3:35pm+2    $883        30h 40m    
   2:15pm      11:10am+1   + $0        32h 55m    
   7:40am      11:10am+1   + $0        39h 30m    
   6:30pm      11:10am+1   + $47       28h 40m    
   4:40pm      11:10am+1   + $47       30h 30m    
   9:30pm      10:30pm+1   + $245      37h 0m     
8:55pm      5:25pm+2    $883        32h 30m    
   2:15pm      11:10am+1   + $0        32h 55m    
   7:40am      11:10am+1   + $0        39h 30m    
   6:30pm      11:10am+1   + $47       28h 40m    
   4:40pm      11:10am+1   + $47       30h 30m    
   9:30pm      10:30pm+1   + $245      37h 0m     
8:55pm      11:00pm+2   $883        38h 5m     
   2:15pm      11:10am+1   + $0        32h 55m    
   7:40am      11:10am+1   + $0        39h 30m    
   6:30pm      11:10am+1   + $47       28h 40m    
   4:40pm      11:10am+1   + $47       30h 30m    
   9:30pm      10:30pm+1   + $245      37h 0m     
10:55pm     11:30pm+2   $995        36h 35m    
   7:10pm      4:00pm+1    + $0        32h 50m    
   1:00am      4:00pm      + $194      27h 0m     
   9:30pm      10:30pm+1   + $439      37h 0m     
   10:35am     8:35pm      + $528      22h 0m     
   4:55am      2:25pm      + $568      21h 30m
