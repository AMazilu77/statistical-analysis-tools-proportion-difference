import math
from scipy.stats import binom, norm

def get_user_float_input(prompt:str="Enter a floating point number :", default:float=0.0, least:float=None, most:float=None) -> float:
    """
    Get user input and return it as a floating point value. Use a default value if provided. Check that
    the value is between (inclusive) the least and most parameters (if given)
    
    Parameters:
    prompt (str): The prompt to display to the user.
    default: The default value to use if the user does not provide any input.
    least: The lowest floating value that is acceptable (if given, else all are acceptable).
    most: The largest floating point value that is acceptable (else all are OK).
    
    Returns:
    The user's input converted to a floating point value that satisfies the parameters.
    """
    while True:
        try:
            user_input = input(prompt)
            if user_input == '' and default is not None:
                return float(default)
            elif user_input == '':
                print("There is no default value, you must give it a floating point value, try again.")
            else:
              value = float(user_input)
              if least is not None and value < least:
                  print(f"The value you entered, {user_input}, which is {value}, is below the minimum acceptable value of {least}. Please try again.")
                  continue # try again
              if most is not None and value > most:
                  print(f"The value you entered, {user_input}, which is {value}, is more than the maximum acceptable value of {most}. Please try again.")
                  continue # try again
              return value # otherwise it is OK, so return it 
        except ValueError:
            print("Invalid input. Please enter a floating point value.")
            
def get_user_int_input(prompt:str="Enter an integer (whole number) :", default:int=0, least:int=None, most:int=None) -> int:
    """
    Get user input and return it as an integer value. Use a default value if provided. Check that
    the value is between (inclusive) the least and most parameters (if given)
    
    Parameters:
    prompt (str): The prompt to display to the user.
    default: The default value to use if the user does not provide any input.
    least: The lowest integer value that is acceptable (if given, else all are acceptable).
    most: The largest integer value that is acceptable (else all are OK).
    
    Returns:
    The user's input converted to an integer that satisfies the parameters.
    """
    while True:
        try:
            user_input = input(prompt)
            if user_input == '' and default is not None:
                return int(default)
            elif user_input == '':
                print("There is no default value, you must give it an integer value, try again.")
            else:
              value = int(user_input)  
              if least is not None and value < least:
                  print(f"The value you entered, {user_input}, which is {value}, is below the minimum acceptable value of {least}. Please try again.")
                  continue # try again
              if most is not None and  value > most:
                  print(f"The value you entered, {user_input} which is {value}, is more than the maximum acceptable value of {most}. Please try again.")
                  continue # try again
              return value # otherwise it is OK, so return it 
        except ValueError:
            print("Invalid input. Please enter an integer.")
            
def get_user_yes_or_no_input(prompt:str="Enter Y (yes) or N (no)", default:str='N') -> str:
    """
    Get user input and return it as either 'Y' or 'N'. Use a default value if provided. Check that
       the value is either Y (or y or yes or YES or Yes), or an N.
    
    Parameters:
    prompt (str): The prompt to display to the user.
    default: The default value to use if the user does not provide any input.
    
    
    Returns:
    The user's input converted to either 'Y' or 'N'.
    """
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == '' and default is not None:
            return default.upper()
        if user_input in ['y', 'yes']:
            return 'Y'
        if user_input in ['n', 'no']:
            return 'N'
        print("Invalid input. Please enter either Y or N.")


def print_command_codes():
    print("Available command codes (for each loop iteration):")
    print("1 = Calculates the chance for a certain number of successes (or more) given alpha (significance level), for the current N, p values")
    print("2 = Calculates a confidence interval for given N")
    print("3 = Enter a new set of N, p values")
    print("4 = Enter a new set of N, Successes values (p=Successes/N)")
    print("5 = Calculates a p-hat value given a Z value")
    print("6 = Given a confidence interval as an interval, calculate the point estimate and margin of error")
    print("7 = Set a new number of decimal digits for rounding")
    print("8 = Print the command codes list again")
    print("0 = Stop and exit the loop")

def main():
    print("Python difference in proportions helper: Chapter 6.2")
    print("Here are the standard symbols: N1= # in a sample #1, p1=chance of success in sample 1 (p-hat 1)")
    print("  N2= # in a sample #2, p2=chance of success in sample 2 (p-hat 2)")
    print("  d-hat = difference of p1-p2, also the point estimate (mean difference between mean propoprtions)")
    print("  SEd = Standard Error of d-hat (standard deviation in the sampling distribution lf d-hat)")
    r = get_user_int_input("Round to how many decimal places? : ",4,1,9)
    parms_set = False
    future_code=0 # there are no stacked operations that must be called next

    print_command_codes()
    code = get_user_int_input("Enter the command code (0, or 1-8) :",1,0,8)

    while(code > 0):
      if code == 1:
        print("Calculate one sided (1-tail) chance for a certain # of successes, given significance level")
        if parms_set == False: # we do not have the n1, p1 and n2,p2 set 
          print("You must first use command code 3 or 4 to enter either n1,p1 n2,p2 or n1,k1 n2.k2 values")
          future_code = code # return to this code after setting the parameters
          code = get_user_int_input("Enter the command code (0, or 1-8, preferrably 3 or 4) :",4,0,8)
          continue # go back and loop again
        
        successes = get_user_int_input("number of successes to test for: ",None,0,n)
        ratio = float(successes / n) # calculate the p-hat value we are testing for
        print(f"{successes} successes out of {n} tries is a p-hat value of {ratio}")
        z = (ratio-p)/sdev
        print(f"The Z-score for this p-hat of {round(ratio,r)} is {round(z,r)}")
        if ratio > p:
          print(f"Since this is more than the average of {p} we will test on the right, anything too far on the right (less chance) is significant")
          chance = 1 - norm.cdf(z) # for chance on the right, use complement
        else:
           print(f"Since this p-hat is less than the average of {p} we will test on the left, anything too far on the left (less chance) is significant")
           chance = norm.cdf(z) 
        alpha = get_user_float_input("Enter the significance level for your test (alpha): ",None,0.00001,0.5)
        print(f"The chance of getting a sample with {successes} successes out of {n} is {round(chance,r)}")
        if alpha > chance:
          print(f"SIGNIFICANT: Since the chance of {round(chance,r)} is smaller than the alpha limit of {alpha}, this is SIGNIFICANT")
        else:
          print(f"NOT significant: Since the chance of {round(chance,r)} is >= the alpha limit of {alpha}, this is NOT significant") 
      elif code == 2:
        print("Calculate the confidence interval for a given confidence level, such as .98 (98%)")
        if parms_set == False: # we do not have the n1, p1 and n2,p2 set 
          print("You must first use command code 3 or 4 to enter either n1,p1 n2,p2 or n1,k1 n2.k2 values")
          future_code = code # return tmo this code after setting the parameters
          code = get_user_int_input("Enter the command code (0, or 1-8, preferrably 3 or 4) :",4,0,8)
          continue # go back and loop again
        confidence = get_user_float_input("Enter the confidence level as a decimal (not %) : ",None,0.01,0.99999)
        tail = (1 - confidence)/2
        print(f"Only things that have a chance of less than {round(tail,r+2)} on the left (or right) will be outside the interval")
        zstar= abs(norm.ppf(tail)) # calculate the Z-score (absolute value, it will be - on left + on right
        me = abs(zstar * sdev) # the margin of error is always positive, take absolute value
        lower = float(d - me)
        upper = float(d + me) 
        print(f"for a {confidence} (or {confidence*100}%) confidence interval the Z* is {round(zstar,r)}\n   and the Margin of Error is {round(me,r)}")
        print(f"The interval can be given as {round(lower,r)} < p1 - p2 < {round(upper,r)}") 
      elif code == 3:
        print("Enter a new set of n1,p1 and n2,p2 values")
        print(f" Rounding final answers to {r} decimal places (code 7 to change this)")
        n1 = get_user_int_input("N1 (number of observations in sample #1): ",None,2)
        p1 = get_user_float_input("p1 proportion of successes in N1 (prob,p-hat 1)in sample #1): ",None,0.000001,0.999999)
        k1 = int(p1 * n1) # calculate how many successes, just in case  we need it 
        print(f" We have N1={n1} trials with a success probability (proportion) of p1={round(p1,r)} ({k1}/{n1})")
        fail1 = 1 - p1 # chance of a failure
        n2 = get_user_int_input("N2 (number of observations in sample 2): ",None,2)
        p2 = get_user_float_input("p2 proportion of successes in N2 (prob,p-hat 2)in sample #2): ",None,0.000001,0.999999)
        k2 = int(p2* float(n2))
        print(f" We have N2={n2} trials with a success probability (proportion) of p2={round(p2,r)} ({k2}/{n2})")
        fail2 = 1 - p2 # chance of a failure  
        d = p1 - p2
        sdev = math.sqrt(p1*fail1/float(n1)+p2*fail2/float(n2))
        print(f"The point estimate (d-hat) is {round(d,r)} and the standard Error (deviation) SE={round(sdev,r)}")
        parms_set = True
        pbar = (k1+k2)/(n1+n2)
        tstat = d/math.sqrt((pbar*(1-pbar))*(1/float(n1)+1/float(n2)))
        print(f"pbar = {round(pbar,r)} and the test statistic is z={round(tstat,r)}")
        if future_code>0: # if this was started within another operation
          code=future_code # go back to the previous operation that needed parameters first
          future_code=0
          continue # go back to top
      elif code == 4:
        print("enter a new set of n1 trials ,k1 successes (p-hat1 calculated as k1/n1), and n2,k2")
        print(f" Rounding final answers to {r} decimal places (code 7 to change this)")
        n1 = get_user_int_input("N1 (number of observations in sample1): ",None,2)
        k1 = get_user_int_input("K1 (number of successes in sample1): ",None,1,n1)
        p1 = float(k1) / float(n1)
        print(f"We have N1={n1} trials with\n  p1={round(p1,r)} prob of success (={k1}/{n1})")
        failure1 = 1 - p1 # chance of a failure
        n2 = get_user_int_input("N2 (number of observations in sample 2): ",None,2)
        k2 = get_user_int_input("K2 (number of successes in sample 2): ",None,1,n2)
        p2 = float(k2) / float(n2)
        print(f" and N2={n2} trials with\n  p2={round(p2,r)} prob of success (={k2}/{n2})")
        fail2 = 1 - p2 # chance of a failure  
        d = p1 - p2
        sdev = math.sqrt(p1*failure1/float(n1)+p2*fail2/float(n2))
        print(f"The point estimate (d-hat) is {round(d,r)} and the standard Error (deviation) SE= {round(sdev,r)}")
        parms_set = True
        pbar = (k1+k2)/(n1+n2)
        tstat = d/math.sqrt((pbar*(1-pbar))*(1/float(n1)+1/float(n2)))
        print(f"pbar = {round(pbar,r)} and the test statistic is z={round(tstat,r)}")
        altSE = math.sqrt((pbar*(1-pbar))*(1/float(n1)+1/float(n2)))
        if future_code>0: # if this was started within another operation
          code=future_code # go back to the previous operation that needed parameters first
          future_code=0
          continue # go back to top
      elif code == 5:
        print("Calculate d-hat given Z")
        if parms_set == False: # we do not have the n1, p1 and n2,p2 set 
          print("You must first use command code 3 or 4 to enter either n1,p1 n2,p2 or n1,k1 n2.k2 values")
          future_code = code # return to this code after setting the parameters
          code = get_user_int_input("Enter the command code (0, or 1-8, preferrably 3 or 4) :",4,0,8)
          continue # go back and loop again
        z = get_user_float_input("Enter the value of Z (normalized): ",None,-5.0,5.0)  
        x = z*sdev + d
        print(f"A Z value of {z} gives a d-hat value = {round(x,r)} for the current parameters d={d} and Sdev={sdev}")  
      elif code == 6:
        print("given a confidence interval (lower, upper) find the point estimate and margin of error")
        r = get_user_int_input("Round to how many decimal places? : ",3,1,9)
        lower=get_user_float_input("What is the lower limit of the p-hat interval? : ", None, 0.0001, 0.9998)
        upper=get_user_float_input("What is the upper limit of the p-hat interval? : ", None, 0.0002, 0.9999)
        mid = (upper+lower)/2.0 # the point estimate (most likely value) is the mid-point of the interval, average value
        me = upper - mid # the difference from the center to the upper limit is the margin of error value
        print(f"For the interval ({lower},{upper}) the point estimate is {round(mid,r)} \n   and the margin of error is {round(me,r)}")
      elif code == 7:
        r = get_user_int_input("Round to how many decimal places? : ",4,1,9)
      elif code == 8:
        print_command_codes()
      elif code == 0:
        quit()
      else:
        print("invalid code ", code, " . Should be 0 (to exit) or 1 to 8")
        print_command_codes()
      code = get_user_int_input("Enter the command code (0, or 1-8) :",0,0,8)
      
if __name__ == "__main__":
    main()