## Index sheet for Course file

| Sl. No. | Contents | Page No. |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| 1 | Academic calendar of the University | - |
| 2 | Course outline (Syllabus of the course) (template - 1) | - |
| 3 | Lesson plan (template - 2) | - |
| 4 | Timetable (of all sections of that course) | - |
| 5 | Student list (template - 3) (extracted from SAP) | - |
| 6 | Continuous Internal Evaluation (CIE) | - |
| | - Question paper for the CIE components (min - n +1; max - n + 4) To be common across all sections | - |
| | - Scheme of evaluation (common) and rubrics of all components | - |
| | - 2 sample answer scripts/assignments of the students (of each CIE component) (one best script, one average script) | - |
| | - Consolidated marks sheet of CIE (of all components) | - |
| | - List of slow learners (students whose score is less than 40% in a CIE will be termed as slow learners) | - |
| | Remedial class details - Time table of the class to be conducted - Classes work done statement - Retest (Question paper and answer sheets) (which includes the details of the classes taken, retest conducted and the improved marks from the retest to be considered for CIE) | - |
| | - Finalized CIE marks signed by all the students (which is submitted to the exam office) | - |
| 7 | - SA & FI list | - |
| | - Final attendance sheet (mentioning the % of class attended) | - |
| 8 | Semester End Examination (SEE) | - |
| | - Question paper | - |
| | - Scheme of evaluation | - |
| | - Evaluation rubrics | - |
| | - Result sheet of CIE | - |

an initiative of RV EDUCATIONAL INSTITUTIONS

| 9 | Course-end survey (questions to be specific to the course; not more than 8) | - |
|-----|-------------------------------------------------------------------------------|-----|
| 10 | Course attainment | - |

an initiative of RV EDUCATIONAL INSTITUTIONS

## Course outline (Syllabus of the course) (Template - 1)

Course Code: CS2228

Name of the Programme: B.Tech (Hons.)

Name of the Course: Deep Learning

Semester: V

| Course credit | No. of hours per week | Total no. of Teaching hours |
|-----------------|-------------------------|-------------------------------|
| 03 | 2+0+2 | 60 |

## Course Objectives :

- To introduce the foundational concepts of neural networks and their application in classification tasks.
- To explore advanced deep learning architectures such as Convolutional Neural Networks (CNNs) and Recurrent Neural Networks (RNNs) for solving computer vision and sequence modeling problems.
- To develop practical skills in optimizing and deploying deep learning models using industry-standard SDKs such as OpenVINO, SNPE, and TensorRT.
- To build awareness of ethical considerations in deep learning, including bias, fairness, and privacy concerns.
- To foster responsible AI practices through the study of explainable AI, federated learning, and ethical guidelines for AI research.

## Syllabus:

| Module - 1 Introduction to Deep Learning | No. of hours |
|--------------------------------------------|----------------|

Overview of machine learning and deep learning, History and Evolution of Deep Learning. Introduction to Neural networks: Perceptron, Multilayer Perceptron, Backpropagation, Shallow neural networks, deep neural networks, Optimizers: Gradient Descent (GD), Momentum-Based GD, Nesterov Accelerated GD, Stochastic GD, AdaDelta, AdaGrad, RMSProp, Adam, Loss Functions, Introduction to CUDA.

| Module - 2 Convolutional Neural Networks | No. of hours |
|--------------------------------------------|----------------|

Introduction to Convolutional Neural Networks, Layers in CNN, Types of convolutions, Regularization Techniques: L1/L2 regularization, dropout, Early stopping, Data augmentation, A typical CNN structure, Standard CNN models: AlexNet, VGGNet, GoogLeNet, ResNet, Inception.

| Module - 3 Unsupervised Learning and Generative Modeling with | No. of hours |
|-----------------------------------------------------------------|----------------|
| Autoencoders and GANs | 06 |

an initiative of RV EDUCATIONAL INSTITUTIONS

Autoencoder (Types: Linear, CNN-based), Training Autoencoders, Variational Autoencoders (VAE), Introduction to GAN, GAN Architecture (Generator, Discriminator), Applications.

## Module - 4 Sequence-to-sequence models

No. of hours

06

Introduction to Recurrent Neural Networks and their structure, Challenges in RNN (Vanishing and Exploding Gradients), Long-short term memory (LSTM), Gated Recurrent Unit (GRU), Attention mechanism in RNNs, and Transformers.

## Module - 5 Deep Learning SDKs and Ethical Considerations

No. of hours

06

Overview of deep learning SDKs, Importance of optimization and deployment in deep learning, Intel's OpenVINO Toolkit, Qualcomm's SNPE, NVIDIA TensorRT.

| Lab Programs [30 Hours] | Lab Programs [30 Hours] |
|---------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | Write a program to implement a classification problem using an Artificial Neural Network (ANN). (a) Build the model using varying numbers of hidden layers and neurons in each hidden layer. (b) Use different optimizers and compare their accuracies. (c) Apply dropout and compare the results with those obtained without using dropout by varying the dropout rate. (d) Plot graphs to visualize all the results obtained from the above steps (e) Analyze the impact of hyperparameter tuning (e.g., learning rate, batch size) on model performance. |
| 2 | Create a program to implement a Convolutional Neural Network (CNN) for the given dataset. (a) Design a customized CNN model. (b) Experiment with and without Batch Normalization and compare their accuracy. (c) Evaluate the results against at least three different CNN variants. (d) Visualize the results by plotting graphs (e) Investigate techniques for handling potential dataset imbalances or applying advanced data augmentation |
| 3 | Implement a program to build Recurrent Neural Network (RNN) and Long Short-Term Memory (LSTM) models for the given dataset. (a) Create customized RNN and LSTM architectures. (b) Experiment with variants of RNN and LSTM and compare their performance in terms of accuracy. (c) Analyze and compare the results obtained from RNN and LSTM models. (d) Plot graphs to visualize the loss and accuracy metrics. |

an initiative of RV EDUCATIONAL INSTITUTIONS

Develop a program to implement a Convolutional Neural Network (CNN) for the given dataset.

- (a) Construct the CNN model and train it on the dataset.
- 4 (b) Evaluate the model performance and interpret the results using explainable AI techniques: LIME, SHAP, SmoothGRAD, Occlusion, Saliency Maps. (c) Visualize the interpretations through graphical representations.
- 5 Speed up deep learning inference using NVIDIA TensorRT - Classification

| Course outcomes |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CO1: Apply neural networks to perform classification tasks |
| CO2: Implement and Apply Convolutional Neural Networks (CNNs) for image classification. |
| CO3: Apply VAE and GAN for generating the data, particularly for image data. |
| CO4: Utilize Recurrent Neural Network (RNN) architectures for sequence modeling and text generation. |
| CO5: Deploy and optimize deep learning models using SDKs such as OpenVINO, SNPE, and TensorRT on diverse hardware platforms, while evaluating and addressing ethical challenges in Deep Learning |

| Text books | Text books |
|--------------|------------------------------------------------------------------------------------------------------------|
| 1. | Goodfellow, Ian, Yoshua Bengio, and Aaron Courville. Deep learning. MIT Press, 2016, ISBN : 9780262035613. |
| 2. | Zhang, Aston, et al. "Dive into deep learning." Cambridge University Press, 2023, ISBN-13 : 9781009389433. |

| Reference books | Reference books |
|-------------------|-----------------------------------------------------------------|
| 1. | CS231n: Deep Learning for Computer Vision, Stanford University. |
| 2. | CS6910: Deep Learning, IIT Madras. |
| 3. | Practical Deep Learning, Fast.ai (https://course.fast.ai/) |

an initiative of RV EDUCATIONAL INSTITUTIONS

## Lesson plan (Template -2)

| Name of the Programme: | B.Tech (Hons.) | B.Tech (Hons.) |
|-----------------------------------|-------------------------------|-----------------------------|
| Title of the Course: | Deep Learning | Deep Learning |
| Course code | CS2228 | CS2228 |
| Semester: | IV | IV |
| Names of the Course Instructor(s) | | |
| Course credit | No. of hours per week (2+0+2) | Total no. of Teaching hours |
| 03 | 04 Hours | 60 Hours |

| Session | Mod ule No. | Topic | Pedagogy /activities | Pre-reading/re ference |
|-----------|-----------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|--------------------------|-------------------------------------------|
| 1 | Introductory class, Unit 1: Overview of machine learning and deep learning and History and Evolution of Deep Learning | Interactive lecture + Whiteboard | | Textbook1: Chapter 1 Textbook2: Chapter 1 |
| 2 | Lab 1 | Colab Notebook + Project | | |
| 1 | Lab 1 | Colab Notebook + Project | | |
| 4 | 1 Introduction to Neural networks: Perceptron, Multilayer Perceptron | Whiteboard for problem solving (worksheets), Videos for Perceptron, Colab for Multilayer perceptron | Chapter Chapter | Textbook1: 6 Textbook2: 3 |
| 5 | Backpropagation | Whiteboard for derivation problem solving (worksheets) | and Textbook1: Chapter 1 | |
| 1 | Lab 1 | Colab Notebook + Project | | 6 |
| 1 | Lab 1 | Colab Notebook + Project | | 7 |
| 8 | Shallow neural networks, deep | Interactive lecture + Whiteboard | Textbook1: Chapter 6 | |

an initiative of RV EDUCATIONAL INSTITUTIONS

| neural networks | | Textbook2: Chapter 5 |
|------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|-----------------------------------------------------------|
| Optimizers: Gradient Descent (GD), Momentum-Base d GD, Nesterov Accelerated GD, Stochastic GD, | Whiteboard for derivation and problem solving (worksheets) | 9 Textbook1: Chapter 8 Textbook2: Chapter 11 |
| | Colab Notebook + Project | |
| Lab 1 | Colab Notebook + Project | |
| Optimizers: AdaDelta, AdaGrad, RMSProp, Adam | Whiteboard for derivation and problem solving (worksheets) | 12 Textbook1: Chapter 8 Textbook2: Chapter 11 |
| Lab 1 | Colab Notebook + Project | 13 |
| Lab 1 | Colab Notebook + Project | 14 |
| Unit 2: Introduction to Convolutional Neural Networks | Interactive lecture + Whiteboard | 15 Textbook1: Chapter 9 Textbook2: Chapter 6 |
| About the Images, channels | Interactive lecture + Whiteboard | 16 Textbook1: Chapter 9 Textbook2: Chapter 6 |
| Lab 2 | Colab Notebook + Project | 17 |
| Lab 2 | Colab Notebook + Project | 18 |
| Layers in CNN | Problem solving using worksheets | 2 19 Textbook1: Chapter 9 Textbook2: Chapter 6 Textbook1: |
| Types of convolutions, Regularization Techniques: L1/L2 regularization | Interactive lecture + Whiteboard + Problem solving using worksheets | 20 Chapter 9 Textbook2: Chapter 6 |
| Lab 2 | Colab Notebook + Project | 21 |
| Lab 2 | Colab Notebook + Project | 22 |
| dropout, Early stopping, Data augmentation | Interactive lecture + Whiteboard | 23 Textbook1: Chapter 7 Textbook2: Chapter 4 |
| Lab 2 | Colab Notebook + Project | 24 |

an initiative of RV EDUCATIONAL INSTITUTIONS

| Lab 2 | Colab Notebook + Project | 25 |
|-------------------------------------------------------------------|----------------------------------|------------------------------------------------|
| A typical CNN structure, Standard CNN models: AlexNet, VGGNet | Colab Notebook | 26 Textbook1: Chapter 9 Textbook2: Chapter 6 |
| GoogLeNet, ResNet, Inception | Colab Notebook | 27 Textbook1: Chapter 12 Textbook2: |
| Lab 3 | Colab Notebook + Project | 28 |
| Lab 3 | Colab Notebook + Project | 29 |
| Unit 3: Autoencoder | Interactive lecture + Whiteboard | 30 Textbook1: Chapter 14 Textbook2: |
| Types: Linear, CNN-based | Interactive lecture + Whiteboard | 31 Textbook1: Chapter 14 Textbook2: |
| Lab 3 | Colab Notebook + Project | 32 |
| Lab 3 | Colab Notebook + Project | 33 |
| Training Autoencoders | Interactive lecture + Whiteboard | 34 Textbook1: Chapter 4-5 Textbook2: |
| Variational Autoencoders (VAE) | Interactive lecture + Whiteboard | 3 35 Textbook1: Chapter 20 |
| Lab 3 | Colab Notebook + Project | 36 |
| Lab 3 | Colab Notebook + Project | 37 |
| Introduction to GAN, GAN Architecture (Generator, Discriminator), | Interactive lecture + Whiteboard | 38 Textbook1: Chapter 20 Textbook2: Chapter 17 |
| GAN and VAE Loss functions | Interactive lecture + Whiteboard | 39 Textbook1: Chapter 20 Textbook2: |
| Hands-on on VAE and GAN | Colab Notebook + Project | 40 |
| Lab 4 | Colab Notebook + Project | 41 XAI: LIME |
| Lab 4 | Colab Notebook + Project | 42 XAI: LIME |

an initiative of RV EDUCATIONAL INSTITUTIONS

| Unit 4: Sequence-to-Sequ ence Models | Interactive lecture + Whiteboard + Problem solving using worksheets | Textbook1: Chapter 10 Textbook2: Chapter 8 |
|-------------------------------------------|-----------------------------------------------------------------------|-----------------------------------------------|
| Introduction to Recurrent Neural Networks | Interactive lecture + Whiteboard + Problem solving using worksheets | Textbook1: Chapter 10 Textbook2: Chapter 8 |
| Lab 4 | Colab Notebook + Project | XAI: SHAP, SmoothGRAD |
| Lab 4 | Colab Notebook + Project | XAI: SHAP, SmoothGRAD |
| RNN Structure and Challenges in RNN | Interactive lecture + Whiteboard + Problem solving using worksheets | Textbook1: Chapter 10 Textbook2: Chapter 8 |
| Long-short term memory (LSTM), | Interactive lecture + Whiteboard + Problem solving using worksheets | Textbook1: Chapter 6 - 8 Textbook2: Chapter 9 |
| Lab 4 | Colab Notebook + Project | XAI: Occlusion, Saliency Maps |
| Lab 4 | Colab Notebook + Project | XAI: Occlusion, Saliency Maps |
| Gated Recurrent Unit (GRU), | Interactive lecture + Whiteboard + Problem solving using worksheets | Textbook1: Chapter 10 Textbook2: Chapter 9 |
| Attention mechanism in RNNs | Interactive lecture + Whiteboard + Problem solving using worksheets | Textbook1: Chapter 12 Textbook2: Chapter 10 |
| Transformers. | Interactive lecture + Whiteboard + Problem solving using worksheets | Textbook2: Chapter 10 |
| Lab 5 | Colab Notebook + Project | |
| Lab 5 | Colab Notebook + Project | |
| Intel's OpenVINO | Colab Notebook | Dell web content |
| TensorRT | Colab Notebook | NVIDIA web content |
| Lab 5 | Colab Notebook + Project | |

an initiative of RV EDUCATIONAL INSTITUTIONS

| 59 | 5 Lab 5 |
|------|-------------------------------|
| 60 | Capstone Project Development. |

## Assessment and Evaluation

| Continuous Internal Evaluation (CIE) :70% | Continuous Internal Evaluation (CIE) :70% |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| Components of CIE | Weightage of each component |
| CIE-1 - Lab 1, Review 1 & Quiz | 2+8+10 marks out of 70 |
| CIE-2 - Theory | 25 marks out of 70 |
| CIE-3 - Research paper in IEEE format + Plagiarism report - Working code - Final Project Submission through presentation - Lab 2, Lab 3, Lab 4, and Lab 5 | 10 marks out of 70 3 marks out of 70 4 marks out of 70 2+2+2+2 marks out of 70 |

| Semester End Exams (SEE): 30% | Semester End Exams (SEE): 30% |
|---------------------------------|---------------------------------|
| Mode of Exam | Theory |
| Weightage of exam | 30% |

## Course Outcomes- Programme Outcomes Matrix

| Program Outcome Course Outcome | Program Outcome Course Outcome | PO 1 | PO 2 | PO 3 | PO 4 | PO 5 | PO 6 | PO 7 | PO 8 | PO 9 | PO1 0 | PO1 1 | PO1 2 |
|----------------------------------|------------------------------------------------------------|--------|--------|--------|--------|--------|--------|--------|--------|--------|---------|---------|---------|
| CO 1 | CO1: Apply neural networks to perform classification tasks | 3 | 2 | 3 | | 3 | 1 | | | | | | |

an initiative of RV EDUCATIONAL INSTITUTIONS

| CO 2 CO 3 | Apply Convolutiona l Neural Networks (CNNs) for image classification. CO3: Apply VAE and GAN for generating the data, particularly | 3 3 | 2 2 | 3 3 | 2 | 3 2 | 1 | | |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------|-------|-----|-------|-----|----|----|
| CO 4 | data. CO4: Utilize Recurrent Neural Network (RNN) architectures for sequence modeling and text generation. | 3 | 2 | 3 | 2 | 2 | 1 | 1 | 1 |
| CO 5 | CO5: Deploy and optimize deep learning models using SDKs such as OpenVINO, SNPE, and TensorRT on diverse hardware platforms, while evaluating and addressing ethical challenges in Deep Learning | 3 | 2 | 3 | 2 | 2 | 1 | 1 | 1 |

an initiative of RV EDUCATIONAL INSTITUTIONS

## Rubrics for evaluation of CIE (separate for each CIE component)

| Total Marks | Total Marks | 20 |
|------------------|------------------|--------------------------|
| CIE-1 Components | CIE-1 Components | Rubrics for Assessment |
| CIE-1 | Lab 1 | 2 marks |
| CIE-1 | Quiz | 10 marks (Refer Table 1) |
| CIE-1 | Review 1 | 08 marks (Refer Table 2) |

| Total Marks | Total Marks | 25 |
|------------------|------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| CIE-2 Components | CIE-2 Components | Rubrics for Assessment |
| CIE-2 | Theory | The test will be conducted for 25 marks and will be evaluated according to the Scheme of Evaluation prepared by the team of course faculty. |

| Total Marks | Total Marks | 25 |
|------------------|---------------------------------------------------|---------------------------------------------|
| CIE-3 Components | CIE-3 Components | Rubrics for Assessment |
| CIE-3 | Research paper in IEEE format + Plagiarism report | 10 marks out of 70 (Refer Table 3) |
| CIE-3 | Working code | 3 marks out of 70 (Refer Table 4) |
| CIE-3 | Final Project Submission through presentation | 4 marks out of 70 (Refer Table 5) |
| CIE-3 | Lab2, Lab 3, Lab 4, and Lab 5 | 2+2+2+2 = 8 marks out of 70 (Refer Table 6) |

an initiative of RV EDUCATIONAL INSTITUTIONS

## Table 1: Quiz Rubric Statement (10 Marks)

This rubric is for evaluating individual quiz performance in the Deep Learning course.

Quiz The quiz will be conducted for a total of 10 marks. Each question carries variable weightage based on difficulty level / cognitive level. There is no negative marking for wrong answers.

## Table 2: Deep Learning Project Review 1 Rubric (8 Marks)

This rubric evaluates the student's performance in Review 1, which includes Problem Definition and Literature Review.

| Component | Criteria | Excellent (8) | Good (5) | Needs Improvement (2) | Marks |
|---------------------------------|------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------|-----------------------------------------------------------|-----------------------------------------------------------|---------|
| Research Problem Identification | Clearly defined, well-scoped DL problem relevant to real-world or research domain. | The problem is innovative, well-articulated , and feasible. | The problem is understandable but lacks depth or clarity. | Vague, broad, or disconnected from DL context. | /2 |
| Objectives | Objectives align with the problem and are SMART (Specific, Measurable, Achievable, Relevant, Time-bound) . | Clear, well-structured objectives aligned with the problem. | Objectives exist but not fully SMART or well-aligned. | Objectives missing, vague, or not clearly related. | /1 |
| Literature Review Coverage | At least 6-8 recent and relevant papers (preferably IEEE/ACM) are cited. | Comprehensive and current review covering gaps and trends. | Moderate coverage; few recent or relevant works included. | Limited or outdated literature; lacks research relevance. | /2 |
| Critical Analysis | Comparison of prior | Deep insights, gap | Some analysis, but lacks depth | Mostly descriptive; no critical | /2 |

an initiative of RV EDUCATIONAL INSTITUTIONS

| | work, identification of research gaps, justification of chosen approach. | identification, and synthesis evident. | or connection to the problem. | evaluation or insights. | |
|---------------------------|-------------------------------------------------------------------------------------------------------|---------------------------------------------------------|----------------------------------------|-----------------------------------------------------|----|
| Presentation & Formatting | The report is well-organiz ed, properly formatted, and free from grammatical issues. Uses IEEE style. | Professional structure, error-free, and well formatted. | Acceptable formatting with few errors. | Poor formatting, errors, or missing IEEE structure. | /1 |

Table 3: Research Paper Submission Rubric (10 Marks)

| Criteria | Excellent (9-10 M) | Very Good (7-8 M) | Good (5-6 M) | Needs Improvement (0-4 M) |
|------------------------------------------------------------------|-------------------------------------------------------------------------------------|----------------------------------------------------------|-----------------------------------------------------------------------|------------------------------------------------|
| Content Quality, IEEE Formatting & References, Plagiarism Report | Innovative idea, clear objectives, DL theory aligned, IEEE format, <10% plagiarism. | Mostly complete, minor format issues, 10-15% plagiarism. | Basic idea, limited insight, some citation issues, 15-25% plagiarism. | Lacks structure/origin ality, >25% plagiarism. |

## Table 4: Code Evaluation Rubric (3 Marks)

This rubric is used for evaluating short coding assignments or lab submissions.

| Component | Excellent (3 M) | Good (2 M) | Needs Improvement (1-2 M) |
|---------------|------------------------------------------------------------------------|------------------------------------------------|---------------------------------------------|
| Functionality | Code runs correctly, handles edge cases, and produces expected results | Code runs with minor issues or limited testing | Code has significant errors or does not run |

an initiative of RV EDUCATIONAL INSTITUTIONS

| Code Quality | Follows good practices, well-structured, with meaningful variable names | Acceptable structure, some best practices missing | Poorly structured, unclear naming, or hard to read |
|--------------------------|---------------------------------------------------------------------------|-----------------------------------------------------|------------------------------------------------------|
| Use of DL Libraries | Appropriate use of relevant libraries (e.g., TensorFlow, PyTorch, Keras) | Limited use of relevant libraries | Irrelevant or missing DL components |
| Comments & Documentation | Well-commented, README or inline explanation provided | Partial documentation or comments | No comments or documentation |
| Reproducibility | Code is easy to run with clear setup instructions or environment file | Code runs with some effort | Code hard to reproduce or lacks setup details |

## Table 5: Final Project Submission through Presentation (4 Marks)

This rubric evaluates the final project presentation based on clarity, technical depth, results, and communication.

| Criteria | Excellent (4 M) | Good (3 M) | Needs Improvement (1-2 M) |
|-----------------------|----------------------------------------------------------------|-----------------------------------------------|--------------------------------------|
| Problem Understanding | Clearly explains the problem, motivation, and relevance | Basic explanation with some gaps | Unclear or lacks relevance |
| Model & Methodology | Accurate description of DL model, architecture, and tools used | Partial explanation with minor technical gaps | Superficial or incorrect methodology |
| Results & Insights | Strong results with visualizations; well-interpreted | Acceptable results; some insights | Weak or missing results |
| Presentation Skills | Confident, clear, and time-managed delivery | Some hesitation or time management issues | Unclear, rushed, or poorly managed |

an initiative of RV EDUCATIONAL INSTITUTIONS

| Q&A Handling | Accurate and thoughtful responses | Partially correct responses | Unable to address questions |
|----------------|-------------------------------------|-------------------------------|-------------------------------|

## Final Project Submission Guidelines

Course: Deep Learning

Components: IEEE-format Report + GitHub Code Repository

## 1. Project Report Guidelines (IEEE Format)

- Format: The report must strictly follow IEEE Conference paper format, available at: https://www.ieee.org/conferences/publishing/templates.html
- Use A4-size, two-column layout, and Times New Roman font (size 10).
- Maintain IEEE structure: Abstract, Introduction, Related Work, Methodology, Results, Conclusion, References.
- Length: 6 to 8 pages (excluding references).
- Plagiarism Check: Must be less than 15% (use Turnitin, Grammarly, or institutional tool).
- AI Detection Score: AI-generated content must be below 15% (e.g., GPTZero, Copyleaks).
- Citations: IEEE citation style with numbering [1], [2], etc.
- Minimum of 6-8 scholarly references (preferably IEEE, ACM, Springer, Scopus).

## 2. Code Submission Guidelines (GitHub Repository)

- Platform: Upload code to a GitHub repository.
- Recommended Structure:
- ├── README.md (project title, abstract, setup instructions)

- [ ] ├── requirements.txt or environment.yml (dependencies)

- [ ] ├── /data (sample data or dummy files only)

- [ ] ├── /notebooks or /src (scripts or Jupyter Notebooks)

- [ ] ├── /results (output images, charts, logs, etc.)

- └── report.pdf (final IEEE report)

## · README File:

- Include project title, abstract, setup instructions, and usage guide.

an initiative of RV EDUCATIONAL INSTITUTIONS

- Link to the final PDF report.
- Reproducibility:
- Code must run from scratch with minimal effort.
- Include instructions and any pre-trained models or data links.
- Output must align with reported results.

## 3. Submission Checklist

| Item | Requirement |
|--------------------------|---------------------------------|
| Report Format | IEEE 2-column conference format |
| Page Limit | 6-8 pages |
| Plagiarism | Less than 15% |
| AI Content Percentage | Less than 15% |
| References | At least 15-20 scholarly papers |
| GitHub Repository | Public and accessible |
| README with Instructions | Complete and clearly written |
| Reproducible Results | Code runs without errors |

## 4. Deadline &amp; Submission Instructions

- Deadline: 5 days before the last working day.

- Submission Mode: LMS / Google Form / Email

- Files to Submit:

1. Final IEEE-format Report in PDF

2. GitHub Repository Link

Table 6: Lab Execution Rubric (10 Marks)

| Sl. No | Criteria | Measuring Methods | Excellent (10 M) | Good (8 M) | Poor (2 M) |
|----------|----------------------------------------|---------------------|---------------------------------------------------------------|-------------------------------------|------------------------------------------------|
| 1 | Understanding of DL Problem Statements | Observations | In-depth understanding of DL concepts; suitable model chosen. | Intermediate level of understanding | Basic understanding; model acceptable or poor. |

an initiative of RV EDUCATIONAL INSTITUTIONS

| 2 | Code Execution & Efficiency | Observations | Optimized code with appropriate libraries and correct pipeline. | Correct but unoptimized or incomplete/incorrect code. | Correct but unoptimized or incomplete/incorrect code. |
|-----|-------------------------------|----------------|-------------------------------------------------------------------|---------------------------------------------------------|---------------------------------------------------------|
| 3 | Results and Documentation | Observations | Includes visualizations, well-commented code, and outputs. | Partial visual output and documentation. | Missing visual output and documentation. |

Signature of the Course Faculty