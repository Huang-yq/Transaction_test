import sys
import pandas as pd

def get_payer_balance(transactions, spend):
    # Initialize a dictionary to store payer's points balance
    payer_points = {}

    # Use pandas unique to get unique payers
    for payer in transactions["payer"].unique():
        payer_points[payer] = 0

    # Sort the data frame based on the transaction timestamp
    transactions = transactions.sort_values(by='timestamp')

    # Iterate through the sorted data frame
    for index, row in transactions.iterrows():
        payer = row['payer']
        points = row['points']

        #if the points are returned, add to spend so its value can be deducted from later transactions
        if (points <= 0):
            spend -= points
            continue
        
        #if previous transactions are sufficient, add to the payer's balance
        if (spend == 0):
            payer_points[payer] += points
            continue
        
        #if the balance is insufficient, deduct the points from this transaction
        if (spend > points):
            spend -= points
            continue
        
        #if the balance is sufficient, add the remaining amout of points into the payer's balance
        payer_points[payer] += points-spend
        spend=0

    # Return the payer's points balance
    return payer_points

if __name__ == "__main__":
    try:
        spend = int(sys.argv[1])
    except (IndexError, ValueError):
        print("Error: Missing or invalid argument")
        sys.exit(1)
    # Read the amount from the command line argument
    
    
    # Read the CSV file into a pandas data frame
    transactions = pd.read_csv('transactions.csv')
    
    # Get the payer's points balance after the points have been spent
    payer_points = get_payer_balance(transactions, spend)
    
    # Print the payer's points balance
    print(payer_points)
