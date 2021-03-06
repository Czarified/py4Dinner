#! python3
# Py4Dinner.py
# This script creates a meal plan that meets specified nutrition requirements.
# This document is initially just for the planning and pseudo-code phase of the 
# project. Primary development may take place at home.
import datetime
import random
import logging
import json
import os
from recipe_scrapers import scrape_me
# Note: Install recipe_scrapers by running
#       pip install https://github.com/hhursev/recipe-scrapers/zipball/master
import re
import pyperclip
import pprint
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - ' +\
                    '%(levelname)s - %(message)s')

os.chdir('D:\\Czarified\\Documents\\GitHub\\py4Dinner')

### Classes   ###

class Food:
    '''
    A collection of molecules that is edible.
    Name and type should be provided as strings, all other attributes
    provided on creation are numbers.
    '''
    def __init__(self,name=None,type=None,freq=0,cal=0,protein=0,carb=0,\
                fiber=0,fat=0,t=0,serv=1,dict=None):
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
            self.serv = serv
        else:
            for key in dict:
                setattr(self, key, dict[key])
        
    def __repr__(self):
        ''''''
        return '<FoodObj: %s>' % self.name
    
#


### Functions ###

def randomFood(book,meal):
    '''
    Randomly selects a food from the Recipe Book.
    Dependencies: random, logging
    Input is desired recipe book, and meal type.
    Output is a food for the correct meal.
    '''
    food = random.choice(book)
    
    try:
        for i in range(0,len(book)):
            if meal not in food.type:
                logging.debug('Repicking food for ', meal)
                food = random.choice(book)
            else:
                logging.debug('RandomFood picked a correct meal: ' + str(meal))
                break
    except IndexError:
        logging.debug('RandomFood was given book with zero length!')
    
    if food is prevfood:
        logging.info('Prevfood: ' + food.name + ' is same as ' +       \
                     prevfood.name)
        logging.info('randomFood: Picking different option.')
        food = randomFood(RecipeBook,meal)
        
    return food


def pickFood(RecipeBook,meal,calMax,carbMax,calCount,carbCount,        \
            leftovers=[]):
    '''
    Checks a food object with defined daily goals. Warns the user if
    calorie budget is broken, and tries to pick a food within carb budget.
    Makes sure that new food is not the same as prevfood (defined in the
    main program).
    Dependencies: pickFood, random, logging
    Input is recipe book, meal type, daily limits, and
    available leftovers (optional).
    Output is a food that properly fits the meal plan, calorie count,
    and carb count, as well as the remaining daily limits and
    remaining leftovers.
    '''
    templeft = leftovers
    try:
        food = randomFood(templeft,meal)
        templeft.remove(food)
        # logging.debug('Trying to use leftovers: ' + food.name)
    except IndexError:
        logging.debug('PickFood: Try block failed. Leftovers blank?')
        food = randomFood(RecipeBook,meal)
    except:
        logging.debug('PickFood: Try block failed. No indexError! Check code!')
    
    
    # Warn user if calorie budget broken.
    if (calCount+food.cal) < calMax:
        calCount = calCount + food.cal
        logging.info('Day ' + str(i) + ' calCount: ' + str(calCount))
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
                    food = randomFood(leftovers,meal)
                    logging.debug('Trying to use leftovers: ' + food.name)
                except:
                    food = randomFood(RecipeBook,meal)
    
    # Remove the food from leftovers, if that's where it came from.
    try:
        leftovers.remove(food)
        logging.debug('Removed ' + food.name + ' from leftovers.')
    except:
        logging.debug('No leftovers were used.')
    
    logging.debug(' PickFood Completed!! Food picked: ' + food.name)
    return food, calCount, carbCount, leftovers


def getMacros(plan):
    '''
    Determines daily composition of macronutrients.
    Input is a mealPlan object.
    e.g. plan = mealPlan
    Output is a list object. Each row represent a running tally of macros (day),
    and will contain a list of 3 numbers. 1st number is fat, 2nd is protein,
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


def readRecipes(name):
    '''
    Opens Recipe Book file and reads data into the working namespace.
    Dependencies: os, json, Food class.
    Output is a recipe book object.
    '''
    book = []
    bookFile = open(name + '.dat')
    strList = bookFile.readlines()
    for i in range(len(strList)):
        xx = json.loads(strList[i])
        book.append(Food(dict=xx))
        logging.debug('Appended to RecipeBook')
    return book
        
    
def writeRecipes(food,book='RecipeBook.dat'):
    '''
    Appends new recipe for food to the Recipe Book file.
    Unless specified, the book to append to will be 'RecipeBook.dat'.
    Dependencies: os, json
    '''
    bookFile = open(book, 'a')
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
            print(str(book.index(i)) + ': ' + i.name)

            
def newRecipe(url=None):
    '''
    Scrapes the given webpage of all required recipe data and returns a
    new Food class with appropriate attributes.
    Dependencies: recipe_scraper, re, pyperclip
    '''
    if url is None:
        url = pyperclip.paste()
    
    xx = scrape_me(url)
    serv, cal, fat, carb, prot = xx.myInfo()
    tmpType = input('What type of meal is this? ')
    tmpFood = Food(xx.title(), tmpType.capitalize(), 0, cal, prot, carb,\
                    0, fat, xx.total_time(), serv)
    tmpFood.instr = xx.instructions()
    tmpFood.ingr = []
    scraps = xx.ingredients()
    
    
    # Ingredients are returned from the scraper in a generalizes list
    # of strings. In order to count up all required ingredients, this
    # must be reconfigured to the proper Food class format. Changing the
    # scraper method or output in the future would fix this.
    
    measurements = {'teaspoon':'tsp', 'tablespoon':'tbsp',
                    'teaspoons':'tsp', 'tablespoons':'tbsp',
                    'fluid oz':'fl oz', 'cup':'c', 'pint':'pt',
                    'cups':'c', 'pints':'pts', 'quarts':'qts',
                    'quart':'qt', 'gallon':'gal', 'milliliter':'ml',
                    'gallons':'gal', 'liters':'L', 'pounds':'lbs',
                    'millilitre':'ml', 'liter':'L', 'litre':'L',
                    'pound':'lb', 'ounce':'oz', 'milligram':'mg',
                    'ounces':'oz', 'inches':'in', 'grams':'g',
                    'gram':'g', 'kilogram':'kg', 'millimeter':'mm',
                    'centimeter':'cm', 'meter':'m', 'inch':'in'
                    }
    regNum = re.compile(r'''(
        (\d+/?\d*)                       # The ingredient quantity, Grp1
        \s?                              # Separator
        (teaspoon|tablespoon|            # Measurements           , Grp2
         fluid oz|cup|pint|quart|
         gallon|milliliter|millilitre|
         liter|litre|pound|ounce|
         milligram|gram|kilogram|
         millimeter|centimeter|meter|inch)?s?
        \s?                         # Separator
        (.*)                        # The actual ingredient , Grp3
        )''', re.VERBOSE)
    logging.debug('Ingredient list reformatting...')
    for i in scraps:                    # Take the regex match object
        mo = regNum.findall(i)          # and format it for the Food Class.
        # logging.debug(mo)
        if mo == []:
            continue
        else:
            tmpFood.ingr.append(list(mo[0][1:]))
        
    for i in tmpFood.ingr:
        # logging.debug('')
        numstr = i[0]
        if numstr.isnumeric():
            i[0] = float(numstr)            # Convert the string numbers           
        else:
            numl = numstr.split('/')
            i[0] = float(numl[0])/float(numl[1])
        full_mes = i[1]
        try:
            i[1] = measurements[full_mes]   # Shorten measurements
        except KeyError:
            continue
        
    return tmpFood


def combine(Food1, Food2):
    '''
    Combines 2 foods into 1. Adds together any common ingredients, and
    macronutrients.
    Dependencies: None
    Input is 2 Food class objects.
    Output is a new Food class object.
    '''
    comboDict = { 'name':Food1.name + ' & ' + Food2.name,
                  'type':Food1.type,
                  'freq':0,
                  'cal':Food1.cal + Food2.cal,
                  'protein':Food1.protein + Food2.protein,
                  'carb':Food1.carb + Food2.carb,
                  'fiber':Food1.fiber + Food2.fiber,
                  'netCarb':Food1.netCarb + Food2.netCarb,
                  'fat':Food1.fat + Food2.fat,
                  't':{Food1.name:Food1.t, Food2.name:Food2.t},
                  'serv':Food1.serv
                }
    newFood = Food(dict=comboDict)
    newFood.ingr = Food1.ingr
    newFood.ingr.append(Food2.ingr)
    newFood.instr = Food1.instr + '\n\n' + Food2.instr
    return newFood

#


### Global Variables ###
outFile = open('out.txt','w')

calories = 1456    # The program will make sure daily totals stay under this
carbohydrates = 500# The program will make sure daily totals stay under this
people = 2         # How many people will be following the meal plan

#


logging.debug('Start of Program.')
RecipeBook = []         # RecipeBook is the master list of foods
RecipeBook = readRecipes('RecipeBook')

# Note: The program will probably work better if all recipes are 
#       complete meals. For example, create a recipe for "Porkchops with
#       green beans" instead of both a "Porkchops" and a "Green Beans."


# Schedule input is a list of days. Each day is a list of meals
# (Input will not be changed, but lists are more readable than tuples.)
# This test input will plan 4 days

# Note that the order of meals informs priority!
# Meals given later in the row will be more limited in cal and carb.
inPlan = [
    ['Dinner'],
    ['Dinner'],
    ['Dinner'],
    ['Dinner'],
    ['Dinner'],
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
# exmealPlan[0]['Dinner']
# Lunch?
# exmealPlan[0]['Lunch']

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
f = 0
prevfood = None
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
              
        # Pick a random food.
        food,calCount,carbCount, leftovers =                            \
            pickFood(RecipeBook,meal,calories,carbohydrates,calCount,   \
                    carbCount,leftovers=leftovers)
        
        #TODO: Note the frequency of that food.
        f = food.freq
        prevfood = food
        
        # Adding correct number of meals
        if food.serv >= people:
            mealPlan[i][meal].append(food)
            # Add leftovers to the leftovers list.
            for k in range(food.serv - people):
                myleft = food
                myleft.serv = 1         # Split into individual servings.
                myleft.type + 'Lunch'   # Allow it to be used for lunch.
                leftovers.append(myleft)
        elif food.serv < people:
            x = round(people/food.serv)
            mealPlan[i][meal].append(food)
            for k in range(x*food.serv - people):
                myleft = food
                myleft.serv = 1         # Split into individual servings.
                myleft.type + 'Lunch'   # Allow it to be used for lunch.
                leftovers.append(myleft)
    
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
print('\n\nMeal plan created:')
outFile.write('Meal plan created:\n\n')
pprint.pprint(mealPlan)
pprint.pprint(mealPlan,outFile)

print('')
print('Leftovers:')
outFile.write('\n\nLeftovers:\n')
pprint.pprint(leftovers)
pprint.pprint(leftovers,outFile)


#-----------------------------------------------------------------------

#TODO: Format output dictionary for grocery list and menu
print('\n\n')

groceries = {}

# for v in mealPlan[0]['Dinner'][0].ingr:
#   print(v)

for day in mealPlan:
    for k,v in day.items():
        for eachfood in v:
            for i in eachfood.ingr:
                # print(i)
                if i[2] in groceries.keys():
                    # TODO: Add more of the ingr.
                    groceries[i[2]][0] += i[0]
                else:
                    groceries[i[2]] = [i[0], i[1]]
                    
print('\n\nGrocery List:')
outFile.write('\n\nGrocery List:\n')
pprint.pprint(groceries)
pprint.pprint(groceries,outFile)
            
#TODO: Create grocery list and menu files

## Text Method (already used with pprint)
outFile.close()
##


## Graphical Method
names = {}
coords = [(80,267),(80,380),(80,500),(80,615),(80,730)]

i = 0
for day in mealPlan:
    for k,v in day.items():
        if k in 'Dinner':
            logging.debug(k + ': ' + str(v))
            names[coords[i]] = v[0].name
            i += 1

im = Image.open('images\BlankDinner.png')
draw = ImageDraw.Draw(im)
fontsFolder = 'C:\Windows\Fonts'        # Should probably include all fonts in the repo
myfont = ImageFont.truetype(os.path.join(fontsFolder, 'consolab.ttf'), 24)
stmpfnt = ImageFont.truetype(os.path.join(fontsFolder, 'calibrii.ttf'), 16)
            
for k,v in names.items():
    draw.text(k, v, fill='white', font=myfont)
    
draw.text((75,140),'Generated by py4Dinner ' + str(datetime.date.today()), fill='navy', font=stmpfnt)

### TEMP
stats = getMacros(mealPlan)[4]
labels = ['Fat','Protein','NetCarbs']
colors = ['lightcoral','gold','lightskyblue']
plt.pie(stats, colors=colors, labels=labels, autopct='%1.1f%%', shadow=False, startangle=30)
plt.axis('equal')
plt.savefig('foo.png', bbox_inches='tight')
fig = Image.open('foo.png')
fig = fig.resize((460,320),resample=Image.LANCZOS)
fig.save('plot.png')
im.paste(fig,(400,735))
macrotext = ImageFont.truetype(os.path.join(fontsFolder, 'calibri.ttf'), 18)
draw.text((410,745),'Weekly Macros', fill='black', font=macrotext)
draw.line([(408,763),(525,763)], fill='black',width=1)
###

im.save('new.png')
##

