import os
import matplotlib.pyplot as plt

def main(informationdictionary):
	print('\n\n\n\Exporting the .dat and .stk files to a .png starts now. Might give a warning\n\n\n\n')
	
	
		
		
		
		
	speccontent = []
	stkcontent = []
	filenamelist = []

	for file in os.listdir():
		if file.endswith('abs.dat'):
			with open(file) as f:
				speccontent.append(f.readlines())
				filenamelist.append(file)

		elif file.endswith('abs.stk'):
			with open(file) as f:
				stkcontent.append(f.readlines())
				
						
	#
	#       assign raw file contents to energy and intensity lists
	#


	specenergies = []
	specintensities = []
	stkenergies = []
	stkintensities = []
	for speccontentindex in range(speccontent.__len__()):
		specenergies.append([])
		specintensities.append([])
		for line in speccontent[speccontentindex]:
			specenergies[speccontentindex].append(float(line.split()[0]))
			specintensities[speccontentindex].append(float(line.split()[1]))

	for stkcontentindex in range(stkcontent.__len__()):
		stkenergies.append([])
		stkintensities.append([])
		for line in stkcontent[stkcontentindex]:
			stkenergies[stkcontentindex].append(float(line.split()[0]))
			stkintensities[stkcontentindex].append(float(line.split()[1]))


	#
	#           find max and offset
	#


	maximum = 0
	for spectra in range(specintensities.__len__()):
		if max(specintensities[spectra]) > maximum:
			maximum = max(specintensities[spectra])

	#
	#           find x region of interest
	#               look for non-zero values and assign them to the beginning and end

	startxindexes = []
	endxindexes = []

	for spectra in range(specintensities.__len__()):
		for datapoint in specintensities[spectra]:
			if datapoint > 0:
				startxindexes.append(specintensities[spectra].index(datapoint))
				break
		for dataindex in range(specintensities[spectra].__len__() - 1, 0, -1):
			if specintensities[spectra][dataindex] > 0:
				#print('specintensities[spectra]:\t', specintensities[spectra])
				#templist = specintensities[spectra].reverse()
				#print('templist:\t', templist)
				endxindexes.append(dataindex)
				# here might be a problem:
				# it will give you the FIRST indexed point of this intensity.
				# if the value is doubled it might be earlier

				break

	print(startxindexes)

	startxindex = min(startxindexes)
	endxindex = max(endxindexes)

	startx, endx = specenergies[0][startxindex], specenergies[0][endxindex]
	starty, endy = -maximum/10, maximum * specenergies.__len__() - 1 + maximum/10


	#
	#           plot spectral data
	#


	plt.figure(figsize=(9, specenergies.__len__() * 2.5))
	for spectra in range(specenergies.__len__()):
		plt.axis([startx - 1, endx + (endx - startx)/3 , starty, endy])
		plt.plot(specenergies[spectra], [ (i + spectra*maximum) for i in specintensities[spectra]], linewidth=1)

	for spectra in range(stkenergies.__len__()):
		markerline, stemlines, baseline = plt.stem(stkenergies[spectra], [ (i + spectra*maximum) for i in stkintensities[spectra]], linefmt=None, markerfmt='None', basefmt='None', bottom=spectra*maximum)
		plt.setp(stemlines, 'linewidth', 0.5)

		plt.annotate(filenamelist[spectra], (endx + (endx - startx)/15, spectra*maximum + maximum/20))

	plt.savefig('output.png', transparent=True)