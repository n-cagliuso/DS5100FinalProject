# DS5100FinalProject

## Metadata
Author: Nick Cagliuso (nph4zk@virginia.edu)
Project Name: Monte Carlo Simulator

## Synopsis

### Installation
To install the package, enter the line of Bash below in your command line:
```bash
pip install -e.
```

### Importing
To import the package, enter the line of Python below at the beginning of your notebook or .py file:
```python
from montecarlo.montecarlo import *
```

### Creating Dice
Below is an example of creating a die called "FairCoin" using the package's class "DieClass", with two faces: "H" and "T:"
```python
FairCoin = DieClass(['H', 'T'])
```

### Playing Games
Below is an example of creating a game with 3 identical die, "FairCoin," using the package's class "GameClass," and then playing 1,000 games (i.e. roling all 3 die simultaneously 1,000 times):
```python
FairCoinGame = GameClass([FairCoin, FairCoin, FairCoin])
FairCoinGame.play(1000)
```

### Analyzing Games
Below is an example of analyzing the previous game, "FairCoinGame," using the package's class "AnalyzerClass." "FairCoinAnalysis.jackpot()" returns the number of times in the 1,000 plays that all three die landed on the same face. "FairCoinAnalysis.combo" returns a dataframe showing every combination of three faces landed on over the 1,000 plays, as well as their count. "FairCoinAnalysis.face_counts_per_roll()" returns a dataframe with each face as a column, each roll as a row, and each observation as a count of the frequency of the face across all three dice for that corresponding roll number.
```python
FairCoinAnalysis = AnalyzerClass(FairCoinGame)
FairCoinAnalysis.jackpot()
FairCoinAnalysis.combo()
FairCoinAnalysis.face_counts_per_roll()
```

## API Description

### Classes, Methods, and Attributes
DieClass:  A die has N sides, or “faces”, and W weights, and can be rolled to select a face.
* W defaults to 1.0 for each face but can be changed after the object is created (see 'weight_change' method).
* Note that the weights are just numbers, not a normalized probability distribution.
* The die has one behavior, which is to be rolled one or more times.
* Note that what we are calling a “die” here can be any discrete random variable associated with a stochastic process, such as using a deck of cards or flipping a coin or speaking a language.
* Our probability model for such variable is, however, very simple – since our weights apply to only to single events, we are assuming that the events are independent. This makes sense for coin tosses but not for language use.

Initializer method: An initializer takes an array of faces as an argument. The array's data type (dtype) may be strings or numbers. 
* Internally Initializes the weights to 1.0 for each face.
* Saves both faces and weights into a private dataframe (faces_weights) that is to be shared by the other methods.
    * Attributes:
        * self.faces: input from user when instatiating class
        * self.weights: float of 1.0 applied to each face
        * self.die_info = dictionary of the die's faces and weights from above 

"weight_change" method: A method to change the weight of a single side.
* Takes two arguments: the face value to be changed (face_value) and the new weight (new_weight).
* Checks to see if the face passed is valid; is it in the array of weights (see if statement)?
* Checks to see if the weight is valid; is it a float? Can it be converted to one?

    * Attributes:
        * self.face_value: Face inputted from user when calling method
        * self.new_weight: Weight inputted from user which will be applied to corresponding face; converted to float
        
"die_roll" method: A method to roll the die one or more times.
* Takes a parameter of how many times the die is to be rolled; defaults to 1.
* This is essentially a random sample from the vector of faces according to the weights.
* Returns a list of outcomes.
* Does not store internally these results.
    
    * Attributes:
        * self.rolls_number = integer from user input when calling method; defaults to 1
        * self.total_weights = sum of all the weights for die created in this class
        * self.probabilities = proportional probabilities of landing on each face, given weights (i/total_weights for i in private dataframe)
  
"current_die" method:A method to show the user the die’s current set of faces and weights (since the latter can be changed).
* Returns the dataframe created in the initializer.


GameClass: A game consists of rolling of one or more dice of the same kind one or more times.
* Each game is initialized with one or more of similarly defined dice (Die objects).
* By “same kind” and “similarly defined” we mean that each die in a given game has the same number of sides and associated  faces, but each die object may have its own weights.
* The class has a behavior to play a game, i.e. to rolls all of the dice a given number of times.
* The class keeps the results of its most recent play.

Initializer method: An initializer which takes a single parameter, a list of already instantiated similar Die objects.

* Attributes:
    * self.dice: list of die object created from previous class  
    
"play" method: A play method which takes a parameter to specify how many times the dice should be rolled (number_rolls).
* Saves the result of the play to a private dataframe of shape N rolls by M dice (play_results).
* The private dataframe should have the roll number as a named index.
* This results in a table of data with columns for roll number, the die number (its list index), and the face rolled in that instance.

    * Attributes:
        * self.number_rolls: user input when calling this method
    
"show" method: A method to show the user the results of the most recent play.
* This method just passes the private dataframe to the user.
* Takes a parameter to return the dataframe in narrow or wide form.
* This parameter defaults to wide form.
* This parameter should raise an exception of the user passes an invalid option (see if statement).
* The narrow form of the dataframe will have a twocolumn index with the roll number and the die number, and a column for the face rolled.
* The wide form of the dataframe will a single column index with the roll number, and each die number as a column
    
    * Attributes:
        * self.form: user input when calling this method; must be string 'wide' or 'narrow'
        * self.wide = public verison of private dataframe which stores results from "play" method
        * self.narrow = narrow version of public dataframe which stores results from "play" method (see method docstring)

AnalyzerClass: An analyzer takes the results of a single game and computes various descriptive statistical properties about it. These properties results are available as attributes of an Analyzer object. Attributes (and associated methods) include:
* A face counts per roll, i.e. the number of times a given face appeared in each roll. For example, if a roll of five dice has all sixes, then the counts for this roll would be 6 for the face value '6' and 0 for the other faces.
* A jackpot count, i.e. how many times a roll resulted in all faces being the same, e.g. all one for a six-sided die.
* A combo count, i.e. how many combination types of faces were rolled and their counts.

Initializer method: An initializer which takes a game object as its input parameter.
* At initialization time, it also infers the data type of the die faces used.

    * Attributes:
        * self.game: user input of game created from previous class
        * self.wide: same public dataframe as created in GameClass' "show" method

"jackpot" method: A jackpot method to compute how many times the game resulted in all faces being identical.
* Returns an integer for the number of times to the user.
* Stores the results as a dataframe of jackpot results in a public attribute (jackpot_results).
* The dataframe should have the roll number as a named index.

    * Attributes: 
        * self.jackpot_results: version of self.wide dataframe which includes a column with '1' or '0' values for whether all die on one roll show the same face
        
"combo" method: A combo method to compute the distinct combinations of faces rolled, along with their counts.
* Combinations should be sorted and saved as a multicolumned index.
* Stores the results as a dataframe in a public attribute (face_results).

    * Attributes:
        * self.combo_results: self.jackpot_results dataframe without the 'Jackpot?' column
        * self.face_results: public dataframe with each roll result as the index, and one column with the frequency of that corresponding roll result across the number of plays

"face_counts_per_roll" method:
* A face counts per roll method to compute how many times a given face is rolled in each event.
* Stores the results as a dataframe in a public attribute (face_counts).
* The dataframe has an index of the roll number and face values as columns (i.e. it is in wide format).

    * Attributes
        * self.combo_results: same dataframe as that created in "combo" method
        * self.face_counts: dataframe with a column for each of the analyzed die's faces, and a row for each roll number. Observations are counts of the frequency of a given facing showing up for each roll number

## Manifest

/DS5100 Final Project
    /montecarlo
        __init__.py
        montecarlo.py
    /montecarlo.egg-info
        dependency_links.txt
        PKG-INFO
        SOURCES.txt
        top_level.txt
    FinalProjectReport.ipynb
    LICENSE
    montecarlo_demo.ipynb
    montecarlo_results.txt
    montecarlo_tests.py
    README.md
    setup.py
        