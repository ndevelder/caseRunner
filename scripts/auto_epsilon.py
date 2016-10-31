#!/usr/bin/env python
# Find epsilon boundary conditions

from subprocess import call
import os,sys
import numpy as np

# Function to replace epsilon expression
def replace_eps(case,cl,ce,l,rp,cc,epsName):
	epsFile = case+'/0/epsilon'

	f = open(epsFile,'r')
	filedata = f.read()
	f.close()

 	if (rp < 25.0):
		Sr = pow(50.0/float(rp),2)
	else:
		Sr = 100.0/float(rp)

	if epsName == 'hellsten':
		EpsExpression = str(cc)+'*'+str(Sr)+'*'+'pow((nu+0.833*nut)*mag(vorticity),2)/nu'
	elif epsName == 'eca':
		EpsExpression = str(ce)+'*pow(internalField(k),1.5)/(0.41*'+str(ce)+'*'+str(l)+')'
	else:
		EpsExpression = str(cc)+'*'+str(Sr)+'*'+'pow((nu+0.833*nut)*mag(vorticity),2)/nu'   
	
	newdata = filedata.replace("<valueExpressionHere>",EpsExpression)

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

# Input arguments
epsType=sys.argv[1]
submitJob=sys.argv[2]
decomposeJob=sys.argv[3]

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
<<<<<<< HEAD
rPlus 	    = np.array([999.9])
constantC   = np.array([0.999])
=======
rPlus 	    = np.array([20.0,45.0,70.0,100.0])
constantC   = np.array([0.01,0.1,1.0,2.0,3.0])
>>>>>>> 1fa983a23d8793495d1efc59d7f6e98426b4b415

nCases = rPlus.shape[0]
nCons  = constantC.shape[0]

# Copy and run loop
for c in range(1,nCons+1):
	for n in range(1,nCases+1):
        	newCase = newCasePath+'_'+str(rPlus[n-1])+'_'+str(constantC[c-1])
        	print 'Case: ' + newCase
		result = call('cp -R '+caseTemplatePath+'/ '+newCase,shell=True)

		if result == 0:
			replace_eps(newCase,constantL[n-1],constantE[n-1],lengthScale[n-1],rPlus[n-1],constantC[c-1],epsType)
			replace_tpphi(newCase,phiValue[n-1])

			if decomposeJob == 'decompose':
				decompresult = call('decomposePar -case '+newCase,shell=True)
			
			if decompresult == 0:
				if submitJob == 'submit':
					bsubresult = call('cd '+newCase+' && bsub < job.mpi && cd ..',shell=True)
