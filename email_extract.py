import mailbox
import csv
import codecs

mboxFile = 'mails/NMRT_Form.mbox'
mboxTxt = 'mails/NMRT_Form.txt'
emailResults = 'clean_mail.csv'

emailList = []

def writeToCSV(resultList):

    allRows = []
    x = []
    for a in resultList:
        if a is None:
            x.append('None')
        if len(a) > 0:
            x.append(a)

    allRows.append(x)
    with codecs.open(emailResults, 'a', encoding='utf-8') as out:
        a = csv.writer(out, delimiter=',', quoting=csv.QUOTE_ALL)
        a.writerows(allRows)


def main(debug = 0):
    # debug = int(input("press 1 for debug mode\n"))
    # writer = csv.writer(open("clean_mail.csv", "wb"))

    # things to search for
    searchFor = ['Form submission from: ',
                 'Submitted on ',
                 'First Name: ',
                 'Last Name: ',
                 'Job Title: ',
                 'Institution: ',
                 'Email Address: ',
                 'Phone Number: ']


    searchForLen = len(searchFor)+1

    with codecs.open(mboxTxt, 'r', encoding='utf-8') as file:
        data = file.read()
        mailFile = data


    while mailFile.find(searchFor[0]) > 0:

        if debug == 1:
            with codecs.open('testText.txt', 'w', 'utf-8') as file:
                file.write(mailFile)

        extractedResults = []
        searchCounter = 0
        lastLen = 0
        end = 0

    # for message in mailbox.mbox(mboxFile):
    #     searchCounter = 0
    #     extractedResults = []

        # stM = message.as_string()
        # if debug == 1:
        #     print(stM)

        # determine mentor/mentee using mm
        mm = 0

        for searchSt in searchFor:
            searchCounter += 1

            st = mailFile.find(searchSt)

            if debug == 1:
                print('searchCounter:'+str(searchCounter)+'\t; searching: '+searchSt)
            if st > 0:
                st = st+len(searchSt)
                if debug == 1:
                    print("\tfound at "+str(st))
                if searchCounter < searchForLen:
                    end = mailFile.find('\n', st)
                else:

                    end = mailFile.find('The results of this submission may be viewed at:')
                    if end < st:
                        print("ERROR!")
                        return


                foundVal = mailFile[st:end]
                foundVal = foundVal.replace('\n', ' ').replace('\r', '').strip()
                if searchCounter == 1:
                    if foundVal == 'Application for NMRT Career Mentoring':
                        searchFor.append('What do you hope to contribute through the career mentoring experience?')
                    elif foundVal == 'Application for NMRT Career Mentees':
                        searchFor.append('What do you hope to get out of the career mentoring experience?')
                    else:
                        print("ERROR - cannot determine mentor or mentee!")
                        return

            else:
                if debug == 1:
                    print('Not found')
                foundVal = 'None'
            if debug == 1:
                print('length: ' + str(st) + ':' + str(end) + ', '+searchSt + str(foundVal.encode('utf-8)')))

            extractedResults.append(foundVal)
            lastLen = end + 103

        mailFile = mailFile[lastLen:]
        searchFor.remove(searchFor[-1])

        writeToCSV(extractedResults)
        # if debug == 1:
        #     return extractedResults




        if debug == 1:
            quitYes = 0
            quitYes = str(input('continue? press "y" to break\n'))
            if quitYes == 'y':
                print(1/0)


            # write to CSV file by calling to program

        # return extractedResults

        # input('\nwaiting')


d = str(input("run in debug mode? press 1\n"))
if d == '1':
    main(1)
else:
    main(0)