# 6.00 Problem Set 8
#
# Name:
# Collaborators:
# Time:



import numpy
import random
import pylab
from ps7 import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """      

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """


        # TODO

        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """

        # TODO

        return self.resistances.get(drug, False)




    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        # TODO
        if len(activeDrugs) > 0:
            bIsResistant = False
            for drug in activeDrugs:
                if self.isResistantTo(drug):
                    bIsResistant = True
            if bIsResistant == False:
                raise NoChildException

        if random.random() > self.maxBirthProb * (1 - popDensity):
            raise NoChildException

        newResisList = self.resistances.copy()

        for key in newResisList.keys():
            if newResisList[key] == True:
                if random.random() < self.mutProb:
                    newResisList[key] = False
            else:
                if random.random() < self.mutProb:
                    newResisList[key] = True

        return ResistantVirus(self.maxBirthProb, self.clearProb, newResisList, self.mutProb) 
            

class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        # TODO
        SimplePatient.__init__(self, viruses, maxPop)
        self.drugList = []

    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        # TODO
        # should not allow one drug being added to the list multiple times
        if newDrug not in self.drugList:
            self.drugList.append(newDrug)




    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """

        # TODO

        return self.drugList
        

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        # TODO

        if len(drugResist) <= 0:
            return 0
                
        superVirusCount = 0   
        for virus in self.viruses:
            isResAll = True
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    isResAll = False
            if isResAll:
                superVirusCount += 1
        return superVirusCount

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        # TODO

        virusToClear = []
        virusToAdd = []
        for virus in self.viruses:
            if virus.doesClear() == True:
                virusToClear.append(virus)
        for virus in virusToClear:
            self.viruses.remove(virus)

        popDensity = self.getTotalPop() / float(self.maxPop)

        for virus in self.viruses:
            try:
                newVirus = virus.reproduce(popDensity, self.drugList)
                virusToAdd.append(newVirus)
            except NoChildException:
                pass
        self.viruses.extend(virusToAdd)
        
        return self.getTotalPop()

#
# PROBLEM 2
#

def simulationWithDrug():

    """

    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    # TODO

    virusList = []
    popList = []
    resList = []
    SimNum = 30
    PreStep = 300
    PostStep = 150
    for i in range(100):
        virusList.append(ResistantVirus(0.1, 0.05, {'guttagonol':False}, 0.005))

    for i in range(PreStep + PostStep):
        popList.append(0)
        resList.append(0)

    for i in range(SimNum):

        patient = Patient(virusList, 1000)
        
        for i in range(PreStep):
            virusNum = patient.update()
            resVirusNum = patient.getResistPop(['guttagonol'])
            popList[i] += virusNum
            resList[i] += resVirusNum

        patient.addPrescription('guttagonol')

        for i in range(PreStep,PreStep + PostStep):
            virusNum = patient.update()
            resVirusNum = patient.getResistPop(['guttagonol'])
            popList[i] += virusNum
            resList[i] += resVirusNum

    for i in range(PreStep + PostStep):
        popList[i] /= float(SimNum)
        resList[i] /= float(SimNum)

    x = range(PreStep + PostStep)
    y = popList
    y2 = resList
    pylab.title('Simulation of virus with drugs')
    pylab.xlabel('TimeStep')
    pylab.ylabel('Population')
    pylab.plot(x,y,'r')
    pylab.plot(x,y2,'b')
    pylab.show()

#
# PROBLEM 3
#        

def simulationDelayedTreatment():

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """

    # TODO

    virusList = []
    resultDict = {}
    for i in [0, 75, 150, 300]:
        resultDict[i] = []

    PostStep = 150
    trialNum = 300
    for i in range(100):
        virusList.append(ResistantVirus(0.1, 0.05, {'guttagonol':False}, 0.005))

    for PreStep in resultDict.keys():

        for i in range(trialNum):

            patient = Patient(virusList, 1000)

            for i in range(PreStep):
                patient.update()

            patient.addPrescription('guttagonol')

            for i in range(PostStep):
                patient.update()

            resultDict[PreStep].append(patient.getTotalPop())

    cureList = []
    for i in [0, 75, 150, 300]:
        cure = 0
        for j in resultDict[i]:
            if j < 50:
                cure += 1
        cureList.append(float(cure) / len(resultDict[i]))

    print cureList

    # pylab.subplot(411)
    # pylab.hist(resultDict[0],20)
    # pylab.subplot(412)
    # pylab.hist(resultDict[75],20)
    # pylab.subplot(413)
    # pylab.hist(resultDict[150],20)
    # pylab.subplot(414)
    # pylab.hist(resultDict[300],20)
 
    # pylab.show()
#
# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment():

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    # TODO

    virusList = []
    resultDict = {}
    for i in [0, 75, 150, 300]:
        resultDict[i] = []

    PostStep = 150
    trialNum = 30
    for i in range(100):
        virusList.append(ResistantVirus(0.1, 0.05, {'guttagonol':False, 'grimpex':False}, 0.005))

    for PreStep in resultDict.keys():

        for i in range(trialNum):

            patient = Patient(virusList, 1000)

            for i in range(PostStep):
                patient.update()

            patient.addPrescription('guttagonol')

            for i in range(PreStep):
                patient.update()

            patient.addPrescription('grimpex')

            for i in range(PostStep):
                patient.update()

            resultDict[PreStep].append(patient.getTotalPop())

    pylab.subplot(411)
    pylab.hist(resultDict[0],20)
    pylab.subplot(412)
    pylab.hist(resultDict[75],20)
    pylab.subplot(413)
    pylab.hist(resultDict[150],20)
    pylab.subplot(414)
    pylab.hist(resultDict[300],20)
 
    pylab.show()



#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations():

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        

    """
    #TODO

    virusList = []
    popList = []
    againstList1 = []
    againstList2 = []
    againstListall = []
    SimNum = 30
    for i in range(100):
        virusList.append(ResistantVirus(0.1, 0.05, {'guttagonol':False,'grimpex':False,'ac':False}, 0.005))

    for i in range(300):
        popList.append(0)
        againstList1.append(0)
        againstList2.append(0)
        againstListall.append(0)

    for i in range(SimNum):

        patient = Patient(virusList, 1000)
        
        for i in range(150):
            virusNum = patient.update()
            against1 = patient.getResistPop(['guttagonol'])
            against2 = patient.getResistPop(['grimpex'])
            againstall = patient.getResistPop(['guttagonol', 'grimpex'])
            popList[i] += virusNum
            againstList1[i] += against1
            againstList2[i] += against2
            againstListall[i] += againstall

        patient.addPrescription('guttagonol')
        patient.addPrescription('grimpex')
        patient.addPrescription('ac')

        for i in range(150,300):
            virusNum = patient.update()
            against1 = patient.getResistPop(['guttagonol'])
            against2 = patient.getResistPop(['grimpex'])
            againstall = patient.getResistPop(['guttagonol', 'grimpex'])
            popList[i] += virusNum
            againstList1[i] += against1
            againstList2[i] += against2
            againstListall[i] += againstall

    for i in range(300):
        popList[i] /= float(SimNum)
        againstList1[i] /= float(SimNum)
        againstList2[i] /= float(SimNum)
        againstListall[i] /= float(SimNum)


    pylab.plot(popList,'r')
    pylab.plot(againstList1,'b')
    pylab.plot(againstList2,'g')
    pylab.plot(againstListall,'y')
    pylab.show()





if __name__ == '__main__':
    simulationTwoDrugsVirusPopulations()