# Skyrim Open Animation Replacer Utilities 

Small python scripts for automating bulk changes to OAR/DAR conditions, with a heavy focus on Modern Combat Overhaul movesets.

If anyone stumbles on this you're welcome to use them, I don't intend to post these anywhere just yet, I'm mainly writing this for my own guidance under the assumption I'll actually follow through in development. I should probably be using actual github project features for my roadmap but its already looking as though this could cost me more time than it saves. 

Currently these are quick and dirty fixes but in time I will try to fully utilize the features of OAR like nested structures, variants, and new conditions. To that end I will also need to implement automated conversion from DAR to OAR with submod organization based on the outer folder name - a feature that will only make sense for MO2 users. When we cross that bridge vortex users will have to either designate submod by a range of DAR priorities or educate me on the folder structure for vortex mods as I'm simply not going to install mods on a manager I don't use to provide compatibility for hypothetical users. 

When more have been added I intend to make a simple front end to use as an executable or plugin for mod organizer 2 but for now these can be launched from the Data tab using execute with VFS or the batch scripts can be added as executables. You can also run them from any individual mod folder 

Current uploads only include scripts to add a random condition to add a small amount of variety but I am also working on scripts for stances framework and grip switch handling. 

For now the randomizer just adds an 85% chance condition to slightly adjust variety as a simple test case while I iron out the file search and modification functions. Next steps are to take user input for the random value and be able to modify previously added random conditions as well as limit search to a range of DAR priorities. Next commit will also have a restore backup feature per range of conditions.

Any further changes I think should logically come after OAR conversion so that I can definition a "Condition" type for easy json modification. The randomizer will then traverse each OAR mod for submods with no differences in conditions other than random and reorganize them into variants. If I'm not completely misunderstanding OAR, failing a random check means lower priority mods will be considered next, so I will still need to add a random condition to the submod config to add variance with all OAR mods while also having submod variants. That opens up an enormous number of possible animations 

For stances I can either add desired stance condition AND and a negated OR condition for the other stances to designated submods, or I can actually create a single unified OAR stances mod, copy designated animations to matching folders, and rename the original folders to .mohidden to preserve backups
