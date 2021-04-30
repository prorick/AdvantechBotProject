# Advantech Development

## Some of the scripts I have written for data collection, data cleaning/merging, and recruiting

### Each of these "bots" are simple python scripts. In order to run them, one must have python 3.7 or above installed on their machine, as well as these dependencies installed: pandas, numpy, selenium, fake_useragent, and webdriver_manager.chrome. To install these, simply run: python setup.py develop (within this directory from the command line). Then to run the script, navigate to the directory with the files and run the chosen script (python scriptname.py).
---

### Data Collection
- Script to search through booz allen website and save their company employee information to a csv. 
   - *bah_website_scrape.py*
   - **Results:** With this, was able to save the information of over 300 BAH upper leadership employees, grabbing their names, job description/summary, and broad position title as listed
- Script to hunt linkedin using a backend search query (provided) and save the employees’ names, titles, about paragraphs, desired company experience, and locations. <br>
   - *company_scrape_linkedin.py*<br>
   - Have hunted through: 
      - BAH NAVY, ARMY, USAF 
      - Leidos NAVY, ARMY, USAF 
      - Dynetics NAVY, ARMY, USAF 
   - **Results:** This script has been extremely successful and obtains ~250 employees per different run. Over time, I have added more fields like location, and have been editing the script to match up with the master spreadsheet format. 
- Script to hunt through google using filetype: *** query.
   - *doc_search.py*
   - **Results:** This script was relatively unsuccessful. The webdriver had issues saving certain files and ended up downloading numerous extra junk + duplicates. Still a work in progress if needed.

### Data Cleaning
- Wrote a single script to sequentially: 
   - Split the data into corresponding fields of master spreadsheet 
   - Clean – drop duplicates, drop misc. Info that is irrelevant and wrong, populate expertise field 
   - Merge with the master spreadsheet, double check for dups, and output new master file 
- This sequence was executed each time that new data needed to be entered into a master sheet 
   - *data_merge.py*
   - **Results:** The cleaning process works extremely well. It has been altered over time to line up with the master spreadsheet changes, and is able to consistently merge without issue.
   
### Govwin
- Wrote two scripts to scrape through govwin opportunities (saved or unsaved) and dive into attached documents for each opportunity. If an attachment posted matched something in or “keyword list”, the script downloads the file to the pc in a folder with the OP ID as the title 
   - *govwinscrape_nonsaved_opps.py*
   - *govwinscrape_saved_opps.py*
   - **Results:** The govwin bots exectuted perfectly and ran through a total of near 3000 opportunities. However, they did tend to pick up and save some extra files that did not end up being relevant. This is because I had to keep the criteria relatively broad in order to capture some edge-cases, but in the end resulted in some manual checking and deleting of irrelevant files. 
- Wrote a script to parse through govwin opportunities in San Diego with Leidos as incumbent (these can both be changed) and flag them to saved opportunities if they fell within a certain date range  
   - *govwin_flag_ops.py*
   - **Results:** This script worked great, had no issues executing this simple task. Fields can also be narrowed down for later reuse. 
- Script to automate that "advertise your interest" in Govwin for various opportunities. Fields by various provided criteria such as NAICS codes and populates the form for any ops within the next 2 years.
   - *govwin_entry.py*
   - **Results:** Yet to run the actual script for extended time period.

### LinkedIn
- Script to add new connections with a personalized connect message. The script executes a login to a LinkedIn profile, performs a backend LinkedIn query with given criteria, and will go through each person (up to a specified end), grab their names, and send a personalized connection message. 
   - *new_con_v1.py*
   - **Results:** This bot ran perfecty with no hang-ups. Was able to reach the daily connection limit for one user in the first run through.
- Second script as a sort of follow-up to the previous one. New personalized message, better fielding criteria to yield narrower results within a company and attached website and other interesting links in message.  
   - *new_con_v2.py*
   - **Results:** This bot also ran surprisingly well. Was able to start a conversation with many of the new connections obtained from the first bot, and send some interesting media along with it. Looked very human, did not mess up a single name. 
   - Both scripts were executed with various BAH criteria 
- Script to filter through existing LinkedIn connections (with changeable criteria), and invite them to follow the Advantech LI page 
   - *page_con.py*
   - Used BAH criteria
   - **Results:** The script worked great, went through and invited BAH employees in the specified position until our monthly invite limit was reached. 
- Script to filter through existing Linkedin connections and hunt for certain criteria in their personal page. Currently, it looks through their title, about, and experience sections. If they meet the criteria (or it matches), the script will send them an invitation to follow our LinkedIn page.
   - *pagecon_v2.py*
   - **Results:** The script executes perfectly, with interchangeable criteria that  allows us to drill down further than the provided filters from LinkedIn on the connections page. 
