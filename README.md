# email2git

## Background Information

The Linux project's email-based reviewing process is highly effective in filtering open source contributions on their way from mailing list discussions towards Linus Torvalds' Git repository. However, once integrated, it can be difficult to link Git commits back to their review comments in mailing list discussions, especially when considering commits that underwent multiple versions (and hence review rounds), that belong to a multi-patch series, or that were cherry-picked.

As an answer to these and other issues, we created email2git, a patch retrieving system built for the Linux kernel. For a given commit, the tool is capable of finding the email patch as well as the email conversation that took place during the review process.

This repository contains the scripts used to retrieve the original email patch and discussion that introduced linux commits. The data comes from two different sources: the Linux git repository and [patchwork](https://github.com/getpatchwork/patchwork). Patchwork tracks the patches sent to a mailing list and organises the review in a user firendly maner. 

The commit-patch matches are accessible [here](http://mcis.polymtl.ca/~courouble/email2git/). 


## Using Email2git for your Project

If your project uses an email-based contribution workflow, you can use email2git to provide your community with better context around your project's commits. 

Following are the steps I followed to run Email2git on the Linux Kernel. Keep in mind that the Kernel has 700k + commits, which represents a large amount of data to parse. The following steps were implemented to speed up the matching process.

The process is composed of two major steps:

### Email subject matching:

  This steps leverages the patch subject / commit summary concept. Depending on the linux subsystem, the email subject might often be used as the "commit summary" as the patch makes it to the main linux tree. 

  The scripts used to prepare the data are in [subject_data_gen](https://github.com/alexcourouble/email2git/tree/master/subject_data_gen). 

  [commit_subject_generator.py](https://github.com/alexcourouble/email2git/blob/master/subject_data_gen/git/commit_subject_generator.py) reads a git log output and [pwSubjectFull.py](https://github.com/alexcourouble/email2git/blob/master/subject_data_gen/patchwork/pwSubjectFull.py) reads a data dump from the patchwork database.

  These two scripts will generate the datasets used by [subject_matching.py](https://github.com/alexcourouble/email2git/blob/master/subject_matching.py) to execute the subject matching.

### Targeted lines-based matching:

  This step read the author and the files of patches and commit to make targeted patch/git diff line comparisons. 

  In this step, we also have to generate the necessary data with the scripts in [line_data_prep](https://github.com/alexcourouble/email2git/tree/master/lines_data_prep). Once the data is generated, we run [email2git.py](https://github.com/alexcourouble/email2git/blob/master/emaill2git.py) to generate the list of matches. 

  
