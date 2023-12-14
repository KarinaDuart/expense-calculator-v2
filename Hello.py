import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def amount_format_verification(total_person):
    try:
        list_of_total_person = [float(i_amount) for i_amount in total_person.split(",")]
        return list_of_total_person
    except ValueError:
        st.error("Amounts are not valid.")
        return None

def run():
    st.title("Expense Calculator")
    
    friends = st.text_input("Participants' names (separate names by commas):", key="friends_input")
    total_person = st.text_input("How much each participant spent (separate amounts by commas)?", key="total_input")

    if st.button("Calculate", key="calculate_button"):
        if friends and total_person:
            list_of_friends = friends.split(",")
            list_of_total_person = amount_format_verification(total_person)

            if list_of_total_person and len(list_of_friends) == len(list_of_total_person):
                friends = [(i_friend, i_amount) for i_friend, i_amount in zip(list_of_friends, list_of_total_person)]
                total_spent = sum([i_amount for _, i_amount in friends])

                # Calculate even share
                even_share = total_spent / len(friends)

                amount_spent = [i_amount for _, i_amount in friends]
                amount_due = [i_amount - even_share for _, i_amount in friends]

                # Add messages
                for i_friend, friend_balance in zip(list_of_friends, amount_due):
                    if friend_balance < 0:
                        st.write(f"{i_friend} owes {abs(friend_balance):.2f}€")
                    elif friend_balance > 0:
                        st.write(f"{i_friend} overspent by {friend_balance:.2f}€")
                    else:
                        st.write(f"{i_friend} neither owes nor is owed anything")

                # Plotting bar chart
                ind = np.arange(len(list_of_friends))
                width = 0.35

                plt.figure(figsize=(10, 6))

                # Plot expenses
                bars1 = plt.bar(ind, amount_spent, width, label='Spent', color='lightblue')

                # Plot dues or negative expenses
                bars2 = plt.bar(ind + width, amount_due, width, label='Due', color='salmon')

                plt.xlabel('People')
                plt.ylabel('Amount')
                plt.title('Amount spent and due per person')
                plt.xticks(ind + width / 2, list_of_friends)
                plt.legend()

                # Add value labels
                for bars in [bars1, bars2]:
                    for bar in bars:
                        yval = bar.get_height()
                        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, round(yval, 2), ha='center', va='bottom')

                # Render chart in Streamlit
                st.pyplot(plt)
            else:
                st.error("Number of friends is different from the number of amounts spent")

if __name__ == "__main__":
    run()