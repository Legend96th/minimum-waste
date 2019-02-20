# minimum-waste

 This project is made to provide an answer to the stock cutting problem.
 
The problem consists of cutting linear pieces of different sizes from linear stock with different sizes with a minimum waste in the end.

## Usage :
Open "needs" file and modify-it following this template : 
```
max_sizes=stick_size:number_of_theme;stick_size:number_of_theme
needs=stick_size:number_of_theme;stick_size:number_of_theme;
```

The first line represents what the crafter have in stocks, the second one represents what the client needs.
Example : 
```
max_sizes=12:3;10:2
needs=12:1;5:2;6:2;4:3;2:3
```
Then finally just :
```
python3 main.py
```
And you will the optimized stick architecture, the client loss..ect in the "cuts" file.

------
License: [CC-BY-NC](https://creativecommons.org/licenses/by-nc/4.0/)
