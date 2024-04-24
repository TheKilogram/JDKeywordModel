import spacy
from spacy import displacy
nlp = spacy.load("C:\\Users\\TheKilogram\\OneDrive\\Documents\\programs\\AIResume\\Model")

# Test the model with a new job description
test_text = ''' Perform system design reviews for data center applications to ensure partner designs meet NVIDIA guidelines.
    Work on resolving system integration issues related to thermal, mechanical, electrical, PCIe and GPU interconnect interfaces including out-of-band management services.
    Understand system design requirements for High Performance Computing and AI workloads to drive platform configuration guides for x86 and ARM servers.
    Conduct the installation, configuration and bring-up of enterprise server hardware.
    Work directly with our NVIDIA customers, and analyze data to answer questions, reproduce errors, resolve same, or escalate customer issues.
    Be involved in customer interaction, customer communication via conference calls or face to face meetings
    Familiarize yourself with performing hardware debug using oscilloscopes and analyzers to qualify, validate and solve NVIDIA products for customer systems.
    Track and file new bugs, and reproduce issues as needed.
    Create product specifications, hardware design guides, application notes, and other supporting technical collateral.

What We Need To See

    BS or higher in EE, CE or Systems Engineering or equivalent experience.
    4+ years of relevant experience in supporting enterprise datacenter products for x86 and/or ARM architecture.
    Have strong analytical skills and past experience in reviewing enterprise system design and CPU architecture.
    Understanding of x86 and ARM system architecture for server design including BMC, security and out-of-band management.
    Professional-level interpersonal skills, including your ability to adjust your communication to the technical level of the audience.
    An innate capability to accurately and succinctly communicate procedures, results, and recommendations to customers.
    Experience with using lab tools such as oscilloscopes, multi-meters and logic analyzers.
    Possess a nurtured knowledge of Linux, and be very comfortable working in various Linux environments as well as with Windows OS.

NVIDIA is widely considered to be one of the technology world’s most desirable employers. We have some of the most forward-thinking and hardworking people in the world working for us. If you're creative and autonomous, we want to hear from you!
'''
doc = nlp(test_text)
for ent in doc.ents:
    print(ent.text, ent.label_)
#displacy.serve(doc, style="ent")