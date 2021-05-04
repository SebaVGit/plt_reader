# plt_reader python script
A python script that reads and plots PLT files from TECPLOT in Groundwater Vistas.
## Required packages
**pandas version:** `1.1.3 or later`\
**matplotlib version:** `3.3.1 or later`\
**numpy version:** `1.19.2 or later`\
**tqdm version:** `4.49.0 or later`
## Example
As an example I used CLN_TEST.plt file, wich was created with [Groundwater Vistas 7](http://www.groundwatermodels.com/) using `Plot>Tecplot>Export>Target Hydrograph`.\
Also you have the entire GWV test project [here](https://github.com/SebaVGit/mfusg_cln_bin_reader) in the `MODFLOW_Files`.\
You can find the last MODLOFW-USG with Transport executable [here](https://www.gsi-net.com/en/software/free-software/modflow-usg.html)
## Capabilities
You can easily read `.plt files` and plot all your targets.\
In this version, you can customized your plots as you like.
## Disclaimer
This is just a simple version and I have to set it better in order to make it easier to use.
## Running test
Assuming that you are using Anaconda, you can run the script from the command lind with:\
`activate [your environment]`\
`python plt_reader.py`\
Otherwise try to set python to **your path** and run the last line.
## Contact
Please if you want to improve the code feel free to contact me or make a pull request.\
email: `sebastian.vazquez@ug.uchile.cl`\
[Linkedin](https://www.linkedin.com/in/sebasti%C3%A1n-v%C3%A1zquez-gasty-952121181/)
