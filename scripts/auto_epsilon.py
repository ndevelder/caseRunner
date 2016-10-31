#!/usr/bin/env python
# Find epsilon boundary conditions

from subprocess import call
import os
import numpy as np

# Function to replace epsilon expression
def replace_eps(case,cl,ce,l):
	epsFile = case+'/0/epsilon'

	f = open(epsFile,'r')
	filedata = f.read()
	f.close()

	newEpsExpression = str(ce)+'*pow(internalField(k),1.5)/(0.41*'+str(ce)+'*'+str(l)+')'
	newdata = filedata.replace("<valueExpressionHere>",newEpsExpression)

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
caseTemplatePath =  runDir + '/' + caseTemplate

# Set up case runs
constantE   = np.array([1,2])
constantL   = np.array([1,1])
lengthScale = np.array([0.01,0.001])
phiValue    = np.array([0.2,0.4])

nCases = phiValue.shape[0]

# Copy and run loop
for n in range(1,nCases+1):
        newCase = caseTemplatePath+'_eps_'+str(n)
        print 'Case: ' + newCase
	result = call('cp -R '+caseTemplatePath+'/ '+newCase,shell=True)

	if result == 0:
		replace_eps(newCase,constantL[n-1],constantE[n-1],lengthScale[n-1])
		replace_tpphi(newCase,phiValue[n-1])
