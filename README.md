# NovelAgents
 Code for my Bachelor Thesis on a Multi-Agent System writing a novel.
 
 # The Idea
 The idea is to seperate each stage of writing a novel into a task completable by two or more AI agents. 
 The tasks are: 
 - Brainstorming for characters, setting, plot and conflict into readable json strings
 - Plotting what's to happen with the material from the brainstorming stage into a scene structure
 - Writing the given scenes
 - Revising the written scenes

 # What I have so far
 I have two agents who brainstorm characters together. One writes a character into a pre-defined json string, 
 the other gives feedback and tries to make the general statements of the first agent more specific. 
 On my Laptop with 16GB of RAM with two 4.2GB models (olmo2) this takes approximately 10 minutes per character. 
 I can try to improve effiency by not letting the critic give free-form feedback but also write into the json 
 string directly and then reducing the loops needed. 
 Brainstorming two characters needed 1158.61 seconds (~19,3 minutes) during my last trial. I hope I can bring this down somehow. 
 Maybe I can try if an AI society would be faster with this. 
 I also do not know, if the characters are generated with knowledge of the characters generated previously. But for further generation
 of Plot and the like I should load the memory json file into the brainstorming agents. 