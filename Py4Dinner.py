#! python3
# Py4Dinner.py
# This script creates a meal plan that meets specified nutrition requirements.
# This document is initially just for the planning and pseudo-code phase of the 
# project. Primary development may take place at home.
import random
import logging
import json
import os
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - ' +\
                    '%(levelname)s - %(message)s')

os.chdir('D:\\Czarified\\Documents\\Python Scripts')

### Classes   ###

class Food:
    '''
    A collection of molecules that is edible.
    Name and type should be provided as strings, all other attributes
    provided on creation are numbers.
    '''
    def __init__(self,name=None,type=None,freq=0,cal=0,protein=0,carb=0,\
                fiber=0,fat=0,t=0,dict=None):
        '''
        Creates all food attributes, or reads them from the supplied
        dictionary. Supply one or the other, not both!
        '''
        if dict is None:
            self.name = name
            self.type = type
            self.freq = freq
            self.cal = cal
            self.protein = protein
            self.carb = carb
            self.fiber = fiber
            self.netCarb = carb - fiber
            self.fat = fat
            self.t = t
        else:
            for key in dict:
                setattr(self, key, dict[key])
        
    def __repr__(self):
        ''''''
        return '<FoodObj: %s>' % self.__dict__
    
#


### Functions ###

def randomFood(RecipeBook,meal)
    '''
    Randomly selects a food from the Recipe Book.
    Dependencies: random, logging
    Input is desired recipe book, and meal type..
    Output is a food for the correct meal.
    '''
    food = random.choice(RecipeBook)
    
    if food.type != meal:
        logging.debug('Repicking food for day ' + str(i) +      \
                        ', meal ' + meal + '...')
        food = randomFood(RecipeBook,meal)
    return food

def pickFood(RecipeBook,meal,calMax,carbMax,leftovers=[])
    '''
    Checks a food object with defined daily goals. Warns the user if
    calorie budget is broken, and tries to pick a food within carb budget.
    Dependencies: pickFood, random, logging
    Input is recipe book, meal type, daily limits, and
    available leftovers (optional).
    Output is a food that properly fits the meal plan, calorie count,
    and carb count.
    '''
    templeft = leftovers
    try:
        food = random.choice(templeft)
        templeft.remove(food)
        logging.debug('Trying to use leftovers: ' + food.name)
    except:
        randomFood(RecipeBook,meal)
    
    if (calCount+food.cal) < calMax:
        calCount = calCount + food.cal
        logging.debug('Day ' + str(i) + ' calCount: ' + str(calCount))
    else:
        logging.warning('Day ' + str(i) + ' calories over limit! Total:'\
                        + str(calCount+food.cal))
        logging.warning('Was trying to add new ' + meal)
        
    # Try to pick a new food, if carb budget is broken.
    for j in range(len(RecipeBook)):
        if (carbCount+food.netCarb) < carbMax:
            carbCount = carbCount + food.netCarb
            break
        else:
            if j == len(RecipeBook)-1:
                logging.warning('Could not find ' + meal + ' on day '\
                                + str(i) + ' that meets carb requirements!')
                logging.warning('Tried ' + str(j+1) + ' times.')
                break
            else:
                try:
                    food = random.choice(leftovers)
                    logging.debug('Trying to use leftovers: ' + food.name)
                except:
                    food = pickFood(RecipeBook,meal,leftovers)
    try:
        leftovers.remove(food)
        logging.debug('Removed ' + food.name + ' from leftovers.')
    except:
        logging.debug('No leftovers were used.')
    
    logging.debug(' Complete. Food picked: ' + food.name)
    return food, calCount, carbCount

def getMacros(plan):
    '''
    Determines daily composition of macronutrients.
    Input is a mealPlan object.
    e.g. plan = mealPlan
    Output is a list object. Each row represent a day from the plan,
    and will contain a dictionary of 3 numbers. 1st number is fat, 2nd is protein,
    3rd is netCarbs.
    '''
    macros = []
    fat_tot = 0
    prot_tot = 0
    carb_tot = 0
    
    for day in plan:
        for meal in ['Breakfast','Lunch','Snacks','Dinner']:
            fat_tot = fat_tot + food.fat
            prot_tot = prot_tot + food.protein
            carb_tot = carb_tot + food.netCarb
        
        macros.append([fat_tot,prot_tot,carb_tot])
    
    return macros

def readRecipes():
    '''
    Opens Recipe Book file and reads data into the working namespace.
    Dependencies: os, json, Food class.
    '''
    bookFile = open('RecipeBook.dat')
    strList = bookFile.readlines()
    for i in range(len(strList)):
        xx = json.loads(strList[i])
        RecipeBook.append(Food(dict=xx))
        logging.debug('Appended to RecipeBook')
        
    
def writeRecipes(food):
    '''
    Appends new recipe for food to the Recipe Book file.
    Dependencies: os, json
    '''
    bookFile = open('RecipeBook.dat', 'a')
    foodstr = json.dumps(food.__dict__)
    w = bookFile.write(foodstr + '\n')
    bookFile.close()
    
def listFood(book):
    '''
    Prints the names of all recipes in the given recipe book variable.
    Useful to determine what foods are in the working namespace.
    '''
    print(str(len(book)) + ' recipes found.\nDo you want to print them all?')
    x = input('[y/n] ')
    if x.lower() == 'y':
        for i in book:
            print(i.name)
#


### Global Variables ###

calories = 1456    # The program will make sure daily totals stay under this
carbohydrates = 25 # The program will make sure daily totals stay under this

#


logging.debug('Start of Program.')
RecipeBook = []         # RecipeBook is the master list of foods

# Note: The program will probably work better if all recipes are 
#       complete meals. For example, create a recipe for "Porkchops with
#       green beans" instead of both a "Porkchops" and a "Green Beans."

TestDinner1 = Food('TestDinner1','Dinner',0.5,500,10,5,2,10,30)
TestDinner2 = Food('TestDinner2','Dinner',0.5,400,10,10,2,5,30)
TestDinner3 = Food('TestDinner3','Dinner',0.5,300,10,10,10,7,30)
# TestDinner has 3 ingredients. Ingredients will never be changed.
TestDinner1.ingr = ( ('Ingrdnt1',10,'oz'),  # Ingredient 1 needs 10 ounces
                     ('Ingrdnt2',12,'cp'),  # Ingredient 2 needs 12 cups
                     ('Ingrdnt3', 5,''  )   # Ingredient 3 needs 5 each
                   )

## These properties were created on init, repeated here for clarity.                   
# TestDinner1.type = 'Dinner'             # This food is a dinner.
# TestDinner1.freq = 0.5                  # Higher = eat more           ### WIP ###
# TestDinner1.cal = 500
# TestDinner1.protein = 10                # This food has 10g of protein
# TestDinner1.carb = 5                    # This food has 5g of carbs
# TestDinner1.fiber = 2                   # This food has 2g of fiber
# TestDinner1.netCarb = TestDinner1.carb = TestDinner1.fiber
                                          # This food has 3g of net carbs.
# TestDinner1.t = 30                      # This food takes 30 minutes to prep/cook


# Create a new entry in the RecipeBook for testing
RecipeBook.append(TestDinner1)
RecipeBook.append(TestDinner2)
RecipeBook.append(TestDinner3)


# Schedule input is a list of days. Each day is a list of meals
# (Input will not be changed, but lists are more readable than tuples.)
# This test input will plan 4 days, each containing various numbers of "dinners"

# Note that the order of meals informs priority!
# Meals given later in the row will be more limited in cal and carb.
inPlan = [
    ['Dinner','Dinner','Dinner'],
    ['Dinner','Dinner'],
    ['Dinner']
]

# For example, to plan work lunches for a week:
worklunches = [
    ['Lunch'],          # Monday
    ['Lunch'],          # Tuesday
    ['Lunch'],          # Wednesday
    ['Lunch'],          # Thursday
    ['Lunch'],          # Friday
]


# Take input and pick meals to fit.
#-----------------------------------------------------------------------
mealPlan = []                               # Final plan will be a list of dicts
                                            # Each dictionary represents a collection of
                                            # Food classes.

########################################################################
# Example complete mealPlan, for 2 1-meal days:

# Whats for dinner on the first day of the plan?
# list( exmealPlan[0]['Dinner'].name)
# Lunch?
# list( exmealPlan[0]['Lunch'].name)

#            exmealPlan = [
               # {'Dinner': [TestDinner1,TestSide1],
                # 'Lunch':[], 'Breakfast':[], 'Snack':[] },
               # {'Dinner': [TestDinner2,TestSide2],
                # 'Lunch':[], 'Breakfast':[], 'Snack':[] }
#            ]

########################################################################

logging.info('Start of plan-builder ...')
i = 0
leftovers = []
# Since "day" is a row, "i" is a numerical counter of the list index for that day.

for day in inPlan:
    mealPlan.append({})             # Add a dict for that day
    calCount = 0
    carbCount = 0
    for meal in day:
        try:
            mealCheck = mealPlan[i][meal]
        except KeyError:
            mealPlan[i][meal] = []  # Add a list for that meal
        
        # TODO: Pull a weighted, random food that matches the meal type
        
        # Pick a random food.
        food,calCount,carbCount = pickFood(RecipeBook,meal,calories,    \
                                            carbohydrates,leftovers)
        
        #TODO: Note the frequency of that food.
        
        mealPlan[i][meal].append(food)
    
    # Check that all desired meals have been planned.
    for k in ['Breakfast','Lunch','Snacks','Dinner']:
        try:
            mealCheck = mealPlan[i][k]
        except KeyError:
            logging.info('No ' + str(k) + ' found for day ' + str(i))
            mealPlan[i][k] = {}
    
    i += 1

logging.info('        Plan-builder complete!')

#TODO: Ask user if plan is acceptable, and allow manual override.

#-----------------------------------------------------------------------
#TODO: Compile output dictionary


#TODO: Format output dictionary for grocery list and menu


#TODO: Create grocery list and menu files