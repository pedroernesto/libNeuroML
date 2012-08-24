"""
Loading an abstract cell - example with IaFCell

The neuroml element loaded is in this format:

<IaFCell id="iaf" v0 = "-70mV" thresh = "30mV" a ="0.02" b = "0.2" c = "-50.0" d = "2" Iamp="15" Idel="22ms" Idur="2000ms"/>


"""

from neuroml.v2.NeuroMLDocument import NeuroMLDocument
from neuroml.v2 import IaFCell
from neuroml.v2 import Network
from neuroml.v2 import ExpOneSynapse
from neuroml.v2 import Population
from neuroml.v2 import PulseGenerator
from neuroml.v2 import ExplicitInput
from neuroml.v2 import SynapticConnection
from random import random


########################   Build the network   ####################################

nmlDoc = NeuroMLDocument(id="IafNet")

IaFCell0 = IaFCell(id="iaf0", C="1.0 nF", thresh = "-50mV", reset="-65mV", leakConductance="10 nS", leakReversal="-65mV")
nmlDoc.add_iafCell(IaFCell0)

IaFCell1 = IaFCell(id="iaf1", C="1.0 nF", thresh = "-50mV", reset="-65mV", leakConductance="20 nS", leakReversal="-65mV")
nmlDoc.add_iafCell(IaFCell1)


syn0 = ExpOneSynapse(id="syn0", gbase="65nS", erev="0mV", tauDecay="3ms")
nmlDoc.add_expOneSynapse(syn0)


net = Network(id="IafNet")
nmlDoc.add_network(net)

size0 = 5
pop0 = Population(id="IafPop0", component=IaFCell0.id, size=size0)
net.add_population(pop0)

size1 = 5
pop1 = Population(id="IafPop1", component=IaFCell0.id, size=size1)
net.add_population(pop1)

prob_connection = 0.5

for pre in range(0,size0):

    pg = PulseGenerator(id="pulseGen_%i"%pre, delay="0ms", duration="100ms", amplitude="%f nA"%(0.1*random()))
    nmlDoc.add_pulseGenerator(pg)

    net.add_explicitInput(ExplicitInput(target="%s[%i]"%(pop0.id,pre), input=pg.id))

    for post in range(0,size1):
        # fromxx is used since from is Python keyword
        if random() <= prob_connection:
            net.add_synapticConnection(SynapticConnection(fromxx="%s[%i]"%(pop0.id,pre), synapse=syn0.id, to="%s[%i]"%(pop1.id,post)))



newnmlfile = "testNml2.xml"
nmlDoc.write_neuroml(newnmlfile)



###########################  Save to file & validate  #################################


from lxml import etree
from urllib import urlopen

schema_file = urlopen("http://neuroml.svn.sourceforge.net/viewvc/neuroml/NeuroML2/Schemas/NeuroML2/NeuroML_v2alpha.xsd")
xmlschema_doc = etree.parse(schema_file)
xmlschema = etree.XMLSchema(xmlschema_doc)

print "Validating %s against %s" %(newnmlfile, schema_file.geturl())

doc = etree.parse(newnmlfile)
xmlschema.assertValid(doc)
print "It's valid!"