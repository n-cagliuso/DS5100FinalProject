# -*- coding: utf-8 -*-

import pandas as pd

class DieClass:
    """
    A die has N sides, or “faces”, and W weights, and can be rolled to select a face.
    W defaults to 1.0 for each face but can be changed after the object is created (see 'weight_change' method).
    Note that the weights are just numbers, not a normalized probability distribution.
    The die has one behavior, which is to be rolled one or more times.
    Note that what we are calling a “die” here can be any discrete random variable associated with a stochastic process, such as
    using a deck of cards or flipping a coin or speaking a language.
    Our probability model for such variable is, however, very simple – since our weights apply to only to single events, we are
    assuming that the events are independent. This makes sense for coin tosses but not for language use.
    """
    
    def __init__(self, faces=[]):
        """
        An initializer takes an array of faces as an argument. The array's data type (dtype) may be strings or numbers. 
        Internally Initializes the weights to 1.0 for each face.
        Saves both faces and weights into a private dataframe (__faces_weights) that is to be shared by the other methods.
        """
        self.faces = faces
        self.weights = [1.0 for i in self.faces]
        self.die_info = {'faces': self.faces, 'weights': self.weights} 
        self.__faces_weights = pd.DataFrame.from_dict(self.die_info)
           
    def weight_change(self, face_value, new_weight):
        """
        A method to change the weight of a single side.
        Takes two arguments: the face value to be changed (face_value) and the new weight (new_weight).
        Checks to see if the face passed is valid; is it in the array of weights (see if statement)?
        Checks to see if the weight is valid; is it a float? Can it be converted to one?
        """
        self.face_value = face_value
        self.new_weight = float(new_weight)
        if (face_value not in list(self.__faces_weights['faces'])):
            print("The face you have entered is not on your die. Please enter a correct face name.")
        else:
            self.__faces_weights.loc[self.__faces_weights.faces == face_value, 'weights'] = new_weight
        
    def die_roll(self, rolls_number = 1):
        """
        A method to roll the die one or more times.
        Takes a parameter of how many times the die is to be rolled; defaults to 1.
        This is essentially a random sample from the vector of faces according to the weights.
        Returns a list of outcomes.
        Does not store internally these results.
        """
        results = []
        self.rolls_number = int(rolls_number)
        self.total_weights = sum(self.weights)
        self.probabilities = [i/self.total_weights for i in self.__faces_weights['weights']]
        self.__faces_weights['Probabilites'] = self.probabilities
        for i in range(rolls_number):
            result = self.__faces_weights.faces.sample(weights = self.__faces_weights.Probabilites).values[0]
            results.append(result)
        return results
        
    def current_die(self):
        """
        A method to show the user the die’s current set of faces and weights (since the latter can be changed).
        Returns the dataframe created in the initializer.
        """
        return self.__faces_weights

class GameClass:
    """
A game consists of rolling of one or more dice of the same kind one or more times.
Each game is initialized with one or more of similarly defined dice (Die objects).
By “same kind” and “similarly defined” we mean that each die in a given game has the same number of sides and associated  faces, but each die object may have its own weights.
The class has a behavior to play a game, i.e. to rolls all of the dice a given number of times.
The class keeps the results of its most recent play.
    """
    
    def __init__(self, dice = []):
        """
An initializer
Takes a single parameter, a list of already instantiated similar Die objects.
        """
        self.dice = dice
    
    def play(self, number_rolls):
        """
A play method
Takes a parameter to specify how many times the dice should be rolled (number_rolls).
Saves the result of the play to a private dataframe of shape N rolls by M dice (__play_results).
The private dataframe should have the roll number as a named index.
This results in a table of data with columns for roll number, the die number (its list index), and the face rolled in that instance.     
        """ 
        self.number_rolls = int(number_rolls)
        results = []
        for i in self.dice:
            result = i.die_roll(number_rolls)
            results.append(result)
            self.__play_results = pd.DataFrame(results).transpose()
            self.__play_results.index.name = 'Roll Number'
            self.__play_results.columns.name = 'Dice Number'
        
    def show(self, form = 'wide'):
        """
A method to show the user the results of the most recent play.
This method just passes the private dataframe to the user.
Takes a parameter to return the dataframe in narrow or wide form.
This parameter defaults to wide form.
This parameter should raise an exception of the user passes an invalid option (see if statement).
The narrow form of the dataframe will have a twocolumn index with the roll number and the die number, and a column for the face rolled.
The wide form of the dataframe will a single column index with the roll number, and each die number as a column
        """
        self.form = str(form)
        self.wide = self.__play_results
        self.narrow = pd.DataFrame(self.__play_results.unstack())
        if self.form == 'wide':
            return self.wide
        elif self.form == 'narrow':
            return self.narrow
        else:
            raise ValueError("Please enter 'narrow' or 'wide' as your desired dataframe output.")
                             
class AnalyzerClass:
    """
An analyzer takes the results of a single game and computes various descriptive statistical properties about it. These properties results are available as attributes of an Analyzer object. Attributes (and associated methods) include:

A face counts per roll, i.e. the number of times a given face appeared in each roll. For example, if a roll of five dice has all sixes, then the counts for this roll would be 6 for the face value '6' and 0 for the other faces.

A jackpot count, i.e. how many times a roll resulted in all faces being the same, e.g. all one for a six-sided die.

A combo count, i.e. how many combination types of faces were rolled and their counts.
    """
    
    def __init__(self, game):
        """
An initializer
Takes a game object as its input parameter.
At initialization time, it also infers the data type of the die faces used.
        """
        self.game = game
        self.wide = self.game.wide
        self.wide.infer_objects().dtypes
        
    def jackpot(self):
        """
A jackpot method to compute how many times the game resulted in all faces being identical.
Returns an integer for the number of times to the user.
Stores the results as a dataframe of jackpot results in a public attribute (jackpot_results).
The dataframe should have the roll number as a named index.        
        """
        self.game.wide['Jackpot?'] = self.game.wide.eq(self.game.wide.iloc[:, 0], axis = 0).all(1).astype(int)
        self.jackpot_results = self.game.wide
        return self.game.wide['Jackpot?'].sum()
        
    def combo(self):
        """
A combo method to compute the distinct combinations of faces rolled, along with their counts.
Combinations should be sorted and saved as a multicolumned index.
Stores the results as a dataframe in a public attribute (face_results).
        """
        self.combo_results = self.game.wide.drop('Jackpot?', axis = 1)
        self.face_results = self.combo_results.apply(tuple, axis = 1).value_counts()
        self.face_results = pd.DataFrame(self.face_results)
        return self.face_results
    
        #combo_copy = self.game.show_results().copy()
        #self.combo_results = combo_copy.value_counts().to_frame('counts')
        
    def face_counts_per_roll(self):
        """
A face counts per roll method to compute how many times a given face is rolled in each event.
Stores the results as a dataframe in a public attribute (face_counts).
The dataframe has an index of the roll number and face values as columns (i.e. it is in wide format).       
        """
        self.combo_results = self.combo_results
        self.face_counts = self.combo_results.apply(pd.Series.value_counts, axis=1).fillna(0).astype(int)
        self.face_counts.columns.names = ['Faces']
        return self.face_counts
    
if __name__ == '__main__':
    test_object = DieClass(['A', 'B', 'C', 'D'])
    test_object.weight_change('B', 2.0)
    test_object.die_roll(3)
    test_object.current_die()
    test_object2 = DieClass(['A', 'B', 'C', 'D'])
    test_object2.weight_change('C', 3.0)
    test_object2.die_roll(2)
    test_object2.current_die()
    test_object3 = GameClass([test_object, test_object2])
    test_object3.play(3)
    test_object3.show('wide')
    test_object4 = AnalyzerClass(test_object3)
    test_object4.jackpot()
    test_object4.combo()
    test_object4.face_counts_per_roll()        