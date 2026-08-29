an initiative of RV EDUCATIONAL INSTITUTIONS

Course Code: CS1120

Name of the Programme : B.Tech (H.)

Name of the Course: : Embedded System and ARM Microcontroller

Semester: II

| Course credit 3 | No. of hours per week (L + T + P): 2:0:2 | Total no. of Teaching hours : 60 |
|-------------------|--------------------------------------------|------------------------------------|

## Course Objectives :

- a) Introduce the fundamentals of embedded systems, including architecture, memory organization, and real-time design constraints.
- b) Gain proficiency in programming RP2040 microcontrollers using C and Assembly for GPIO and peripheral interfacing.
- c) Guide them to analyze and implement embedded applications using ARM Cortex-M instructions, parameter passing, and interrupt handling
- d) Facilitate hands-on learning in building reliable embedded solutions by applying integrated knowledge through lab experiments involving sensors, logic operations, and memory-mapped I/O.

## Course outline (Syllabus of the course) - Template - 1

## Syllabus:

## Module - 1

No. of hours

6

Introduction to Embedded Systems and Memory: Basic embedded system design: Characteristics and design challenges, Types of memory and memory mapping of a typical C program: Code, data, and stack.

## Module - 2

No. of hours

7

Programming GPIOs on Raspberry Pi Pico: System overview of RP2040: Salient features,Developing programs to control LEDs through GPIOs on Raspberry Pi Pico, using the Wokwi online board emulator to simulate programs, Running programs on RP2040: Understanding its internal architecture, including AHB-Lite crossbar, SRAM, and SIO.

## Module - 3

No. of hours

8

Overview of ARM architectures and processors: Cortex-A, Cortex-R, and Cortex-M families, ARM Cortex programmer model,Stack implementation in the Cortex-M0+ processor, Basics of pipelining, understanding and interpreting arithmetic, MOV, Bx instructions, and conditional flags in branch instructions.

an initiative of RV EDUCATIONAL INSTITUTIONS

| Module - 4 | No. of hours 5 |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Advanced Assembly Programming : Writing assembly programs using ADD, SUB, LDR and STR instructions, Parameter passing to functions from high-level languages, Application Binary Interface (ABI) and AAPCS (ARM Procedure Call Standard),Developing programs using CMP, LDR, STR, and logical instructions. | Advanced Assembly Programming : Writing assembly programs using ADD, SUB, LDR and STR instructions, Parameter passing to functions from high-level languages, Application Binary Interface (ABI) and AAPCS (ARM Procedure Call Standard),Developing programs using CMP, LDR, STR, and logical instructions. |

| Module - 5 | No. of hours 4 |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Peripherals Programming : Using Push, and Pop instructions to write assembly programs, Developing applications using SDK, Software development using I2C and DMA modules. Introduction to ISR. | Peripherals Programming : Using Push, and Pop instructions to write assembly programs, Developing applications using SDK, Software development using I2C and DMA modules. Introduction to ISR. |

| Course outcomes | Course outcomes |
|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| a) | Understand the concept of embedded system, microcontroller, different components of microcontroller and their interactions as applied to RP2040. |
| b) | Get familiarized with the programming environment to develop embedded solutions. |
| c) | Program ARM microcontroller to perform various tasks and stack implementation in Cortex-M0+. |
| d) | Understand the key concepts of embedded systems such as Instruction cycle execution, I/O, DMA, interrupts and interaction with peripheral devices. |

| Text books | Text books |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | Fundamentals of System-on-Chip Design on Arm Cortex-M Microcontrollers by René Beuchat, Florian Depraz, Andrea Guerrieri, and Sahand Kashani (2021), 1st Edition, ARM Education Media.ISBN-13: 978-1911531333 |
| 2 | Modern System-on-Chip Design on Arm by David J. Greaves (2021), 1st Edition, ARM Education Media.ISBN-13: 978-1911531364 |

| Reference books | Reference books |
|-------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| 1 | Getting started with Raspberry Pi Pico (Apr 2021), RP2040 a microcontroller by Raspberry Pi, 1st Edition, Raspberry Pi (Trading) Ltd. |
| 2 | Raspberry Pi Pico C/C++ SDK (Apr 2021), RP2040 a microcontroller by Raspberry Pi, 1st Edition, Raspberry Pi (Trading) Ltd. |
| 3 | ARM, (2012), Cortex-M0+Technical Reference Manual, ARM Ltd. |

an initiative of RV EDUCATIONAL INSTITUTIONS

| Sl No. | List of Experiments (30 Hours) |
|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | a) Blink the LED_BUILTIN using a blink LED program from examples and Display 'Hello World 'Using the Serial monitor tool. b) Write a program to blink 2 alternate LEDs out of 4 LEDs with delay of 3 and 5 seconds respectively. |
| 2 | a) Write a program to display the numbers in the increasing and decreasing order from 1 to 15 and vice versa in binary form, using 4 LEDs, with a delay of 1 sec. When it reaches the maximum value (15), start counting down to 1, then again begin counting up to 15, then start from 1. Whenever it comes to the Max or Min value, wait for 2 seconds. b) Write a program to display only odd , even numbers in binary form, using 4 LEDs, with a delay of 1 sec. When it reaches the maximum value, wait 2 seconds and start from the minimum. |
| 3 | a) Write an assembly function that just returns 200 back to the C program and write an assembly function that returns sum of three constants 10, 20 and30, and returns the result. b) Write an assembly function that returns sum of four constants 10, 20, 30 and40, and returns the result. c) Write an assembly function that returns sum of five constants 10, 20, 30, 40and 50, and returns the result. |
| 4 | a) Write an ARM assembly function that takes three constants as inputs from C++ program, perform ADD operation, and returns the result to the C++ program. b) Write an ARM assembly function that takes two input parameters, performs an AND, OR logic operation on it, and returns the result to a calling C++ program. c) Write an ARM assembly function that takes one input parameter, performs a bitwise NOT operation on it, and returns the result to a calling C++ program. |
| 5 | a) Write an ARM assembly function that performs 2 times logical shift right operation on one parameter and returns the result to a calling C++ program. b) Write an ARM assembly function that performs 2 times logical shift right and 4 times logical shift left operation on one parameter and returns the result to a calling C++ program. |
| 6 | a) Write an ARM assembly function that performs 8 times arithmetic shift right operation on one signed (Negative number) parameter and returns the result to a calling C++ program. |
| 7 | a) Verify the De-morgans theorem with two inputs. If the result is TRUE, print both the results and 'De-morgans theorem is verified', else, print both the results and 'Demorgans theorem is not verified'. |

an initiative of RV EDUCATIONAL INSTITUTIONS

| | b) Perform EX-OR operation with two inputs. If the result is TRUE, print both the results and 'EX-OR logic expression is verified', else, print both the results and 'EXOR logic expression is not verified'. |
|----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 8 | a) Write ARM assembly functions to take two unsigned parameters and perform an ADD operation. b) Write ARM assembly functions to Read the flag bits from the PSR. Return both outputs to the main function. |
| 9 | Write a program for the Raspberry Pi Pico to transmit and receive data through serial communication (UART) port. Transmitting and Receiving Board (RP2040): UART0, GP0 (UART0 Tx), GP1 (UART0 Rx) |
| 10 | Write a program to control one slave device from one master device using serial communication through the I2C port with the following specifications.Master Slave Board (RP2040): I2C0,GPIO pins: GP0 (I2C0 SDA), GP1 (I2C0 SCL) |