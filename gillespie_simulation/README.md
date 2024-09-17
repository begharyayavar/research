# A fast and exntensible implementation of gillespie simulation

## Prerequisites

    +   grpcio version 1.47
    +   python version 3.11
    +   conda

## How to use

## Reactions Format

- Backward reactions are **not** assumed.They have to be **explicitly** written.

### Formatting

- Whitespace is **not** significant.
  - "A + B --> C" is **equivalent** to "A+B->C".
- **Semi-colons** at the **end** of the line are **necessary**.
- All reactions **must** be written in a **new line**.
- Commenting is supported via **"#"** or **"/"**.

### Species

- You **cannot** have the **same** species on **both sides** of the reaction. <!--Maybe future feature update?-->
- Species are delimited by **"+"** or **","**.
  - "A+2B-->C" is **equivalent** to "A,2B>C".
- All species **must** begin with the **alphabet** and must **not** have **spaces** or **special characters** in the name.
  - **Valid Names:** "Ch2OH", "H20" , "ABcd"
  - **Invalid Names:** "2DMT", "H-O-H", "123"
- Coefficients are **assumed** to be **1**.
- Coefficients **must** be **non negative integers**.
- For **non-zero coefficients**, There **must** be a **"."** **between** the species and coefficient.
  - **Valid Coefficients:** "3.A", "12 . B"
  - **Invalid Coefficients:** "3A", "12 B"

### Reactions

- Products and Reactants can be **diffrentiated** by **">"** or **"->"** or **"-->"**.
- Actually, you can go nuts with the number of dashes.
  - "A+B>C" is **equivalent** to "A+B->C" is **equivalent** to "A+B-------------->C".

### Rate Constants

- Rate constants must be written **after** **"@"** or **"|"**.
- They will be interpreted as **numpy.float** and will be **unitless**.

### Initial Conditions

- Initial specie counts **must** be **non negative integers**.
- Initial specie counts **must** be written in a **new line**.
- The Species must be seperated from the values by **"="** or **":"**.
  - **Correct Way:** "A:12", "B=50"
  - **Incorrect Way:** "A:12;B=50"
- If Initial count is **not specified**, it will be **assumed** to be **0**.

### Simulation Parameters
