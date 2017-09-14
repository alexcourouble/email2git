# email2git

Matching Linux Code with its Mailing List Discussions

This repository contains the code used to retrieve the original email patch and discussion that introduced linux commits.

The data comes from two different sources: the Linux git repository (or your own project) and patchwork.

I was very lucky to be able to query the patchwork.kernel.org database directly, which you might not be anle to do. 

The easiest way for you to collect patch data would probably be to run you own patchwork instance and parse your mailing list archive that way. 

## Executing the scripts

The process is composed of two major steps:

- Email subject matching:

  This steps leverages the patch subject / commit summary concept. Depending on the linux subsystem, the email subject might often be used as the "commit summary as the patch makes it to the main linux tree. 

- Targeted lines-based matching:

  This step read the author and the files of patches and commit to make targeted patch/git diff line comparisons. 

Before each step is executed, you will need to generate the data. The scripts used to generate the data live in the ```lines_data_prep``` and ```subject_data_gen``` directories
