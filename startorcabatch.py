import sys
import os
import plotorcaspecv2

DoTheStuff = True


def StartOrcaCalculation(informationdictionary):

	foldername = informationdictionary['foldername']
	
	print('\n\n=============================\n\n')
	print('working in the folder:', foldername)
	print()
	
	os.chdir(foldername)
	
	
	"""
	in the folder, find input file via searching for .inp file
	assign it to variable "inputfilename"
	"""
	inputfilename = ''
	for root, dirs, files in os.walk(foldername):
		for file in files:
			if file.endswith(".inp"):
				 inputfilename = file

	outputfilename = inputfilename.replace('.inp', '.out')
	


	"""
	remove an old output file if it exists.
	
	try:
		os.remove(inputfilename.replace('.inp', '.out')
	"""

	print('Starting ORCA now, please now. I will let you know and program will continue when ORCA Job is done')
	print('...')
	print()
	
	if DoTheStuff:
		os.system(f"D:\orca501\orca {inputfilename} > {outputfilename} &")
	print('that was the ORCA job, I will continue now.')


	informationdictionary['outputfilename'] = outputfilename
	informationdictionary['inputfilename'] = inputfilename
	
	return informationdictionary


def ExportSpectrumFromOutFile(informationdictionary):
	"""
	checking output file now IF there is a spectrum
	if yes: 
	- get to know the transition regime (find transitions)
	"""
	foldername = informationdictionary['foldername']
	outputfilename = informationdictionary['outputfilename']
	inputfilename = informationdictionary['inputfilename']
	
	with open(outputfilename, 'r') as file:
		content = file.readlines()
	
	for n, line in enumerate(content):
		if line.startswith('         ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS'):
			# this is the line (n) where the (header of the) absorption spectrum table starts
			for k, newline in enumerate(content[n:]):
				if newline == '\n': 
					# this is the line (k) where the absoption spectrum table ends
					startingenergy = float(content[n + 5].split()[1]) / 8065.54429
					endenergy = float(content[n + k - 1].split()[1]) / 8065.54429
					
					print(startingenergy)
					print(endenergy)

					break
			"""
			now that we have the energy regime where the absorption spectrum is
			we will call the orca_mapspc command to create the spectrum
			"""
					
			if DoTheStuff:
				os.system(f"D:\Orca501\orca_mapspc {outputfilename} abs -eV -w0.35 -n5001 -x0{startingenergy - 20} -x1{endenergy + 20}")




if __name__ == "__main__":
    informationdictionary = {}
    # getting the foldername from the cmd line (via the .bat call)
    informationdictionary['foldername'] = sys.argv[1]

    # start the orca calculation
    #  send the informationdictionary to it, but also read it back with new insights (filenames)
    informationdictionary = StartOrcaCalculation(informationdictionary)
	
    # start plotting the spectrum, if there is one
    ExportSpectrumFromOutFile(informationdictionary)
	
	
    # use the .dat and .stk files to create the image
    plotorcaspecv2.main(informationdictionary)
	
	
	
	
    print('finished, exiting now')
    print('\n\n=============================\n\n')
	
	
	
	