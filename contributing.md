# Contributing to Techno-economic optimization module (TEO) of the EMB3RS project
We are very grateful that you are looking into how you can contribute to TEO module of the EMB3RS project. The TEO Module is used to conduct a source sink matching for optimal recovery and use of industrial excess heat. 

Contributing to the TEO module is open to everyone who is interested, and we adopt an inclusive and open policy which is described in our code of conduct

## Some resources:

The main EMB3RS website is a good place to get started with EMB3RS
You can find information on how to donwload the moduel and run it in the read me file on the repository or in the documentation. 

The TEO is based on the open source energy system modeling tool OSeMOSYS
The main OSeMOSYS website is a good place to get started with OSeMOSYS
The forum is a great place to ask questions and search for answers from the knowledgeable community


## Bugs
If you find a programming error in  the TEO Module implementations, please submit an Issue in the  repository. Follow the issue template for submitting a bug.


If you find a more fundamental issue which you think is related with the formulation of TEO please submit the issue at the repository and specify the .

Errors, typos or spelling mistakes in the documentation


## Ideas and Suggestions
If you have a great idea for how the TEO could be improved, or to suggest a useful addition to the model, please submit a feature request.

## Git Workflow
To work with the TEO code bases, please follow the forking workflow recommended for contributing to open-source projects. The steps below assume you have a Github account.

Fork the repository to which you wish to contribute by clicking the grey fork button or visiting https://github.com/EMB3RS-TEO-Module/fork
Clone your fork of the repository git clone http://github.com/<user>/EMB3RS-TEO-Module
Create a new branch on which you will commit your changes git checkout -b <branchname>
Do the work and stage and commit your changes: git add ..., git commit -m "A nice descriptive message"
Push the changes to your fork git push -u <branchname> origin/<branchname>
Submit a pull request from your fork of the repository to the master branch of the original repository.
The pull request is reviewed. Any changes required by the review can be performed on the same branch and pushed to the forked repo as in the steps above.
Once the pull request has been reviewed and accepted, you may delete your local copy of the branch git branch -d <branchname> and update your copy of the master branch git checkout master, git pull origin master
