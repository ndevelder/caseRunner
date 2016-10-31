#!/usr/bin/env python
# Find epsilon boundary conditions

from subprocess import call
import os
import numpy as np

# Function to replace epsilon expression
def replace_eps(case,cl,ce,l,rp,cc):
	epsFile = case+'/0/epsilon'

	f = open(epsFile,'r')
	filedata = f.read()
	f.close()

 	if (rp < 25.0):
		Sr = pow(50.0/float(rp),2)
	else:
		Sr = pow(100.0/float(rp),2)

	hellstenEpsExpression = str(cc)+'*'+str(Sr)+'*'+'pow((nu+0.833*nut)*mag(vorticity),2)/nu'
	newEpsExpression = str(ce)+'*pow(internalField(k),1.5)/(0.41*'+str(ce)+'*'+str(l)+')'
	newdata = filedata.replace("<valueExpressionHere>",hellstenEpsExpression)

	f = open(epsFile,'w')
	f.write(newdata)
	f.close()

# Function to replace tpphi expression
def replace_tpphi(case,value):
        phiFile = case+'/0/tpphi'

        f = open(phiFile,'r')
        filedata = f.read()
        f.close()

        newdata = filedata.replace("<phiReplacementValue>",str(value))

        f = open(phiFile,'w')
        f.write(newdata)
        f.close()


# Source the foam-extend bashrc file
call(['/bin/bash','-i','-c','fe32'])

# Set up case dirs
runDir = os.environ.get('FOAM_RUN')
caseTemplate = 'channel_3d_rough_template'
caseTemplatePath =  runDir + '/caseRunner/' + caseTemplate
newCaseRoot = 'channel_3d_rough_epsTest'
newCasePath = runDir + '/' + newCaseRoot

# Set up case runs
constantE   = np.array([1,1,1,1])
constantL   = np.array([1,1,1,1])
lengthScale = np.array([0.1,0.1,0.1,0.1])
phiValue    = np.array([0.09743541, 0.22499132, 0.31663022, 0.40199916])
rPlus 	    = np.array([20.0,45.0,70.0,100.0])
constantC   = np.array([0.01,0.1,1.0,3.0,5.0])

nCases = phiValue.shape[0]
nCons  = constantC.shape[0]

# Copy and run loop
for c in range(1,nCons+1):
	for n in range(1,nCases+1):
        	newCase = newCasePath+'_'+str(rPlus[n-1])+'_'+str(constantC[c-1])
        	print 'Case: ' + newCase
		result = call('cp -R '+caseTemplatePath+'/ '+newCase,shell=True)

		if result == 0:
			replace_eps(newCase,constantL[n-1],constantE[n-1],lengthScale[n-1],rPlus[n-1],constantC[c-1])
			replace_tpphi(newCase,phiValue[n-1])
