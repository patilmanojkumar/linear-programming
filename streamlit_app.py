import streamlit as st
import pandas as pd
from scipy.optimize import linprog

def optimize_cropping(data):
    # Extracting necessary data
    c = -data['Net Return per Unit'].values  # Objective: Maximize returns
    
    # Constraints
    A = data[['Labor Required', 'Capital Required']].values.T
    b = [50, 200]  # Example constraints for labor and capital
    
    # Binary decision variable for land
    land_required = data['Land Required'].values
    bounds = [(0, 1) if land_required[i] == 1 else (0, 0) for i in range(len(c))]
    
    # Solve the linear program
    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
    
    return result.x, -result.fun

def main():
    st.title("Crop Optimization using Linear Programming with Binary Land Allocation")
    
    # Upload Excel file
    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
    if uploaded_file:
        data = pd.read_excel(uploaded_file)
        st.write("Uploaded Data:", data)
        
        # Optimization
        allocation, max_return = optimize_cropping(data)
        st.write("Optimal Cropping Pattern:", allocation)
        st.write("Maximum Net Return:", max_return)
        
        # Sensitivity Analysis (simplified example)
        st.write("Sensitivity Analysis:")
        for i in range(len(allocation)):
            st.write(f"Crop {data['Crop'][i]}: Allocate {'Yes' if allocation[i] > 0.5 else 'No'}")

if __name__ == "__main__":
    main()
