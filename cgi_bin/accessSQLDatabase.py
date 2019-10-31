import cgi
import cgitb
import sys
import searchSQLDatabase


def returnError(errorString):
    print("""<html><body> <h3 id="results_table" style="color:red;">%s</h3> </body></html>""" % errorString)


cgitb.enable()

print("Content-type: text/html")
print("")
print('<!DOCTYPE html>')

# Get the form data
form = cgi.FieldStorage()
if not (form.has_key("option")):
    returnError("No option input?")
    sys.exit(0)

optionInput = form["option"].value

# Check if option selected is location
if optionInput == "location":

    if not (form.has_key("name")):
        returnError("No name input?")
        sys.exit(0)

    nameInput = form["name"].value
    if len(str(nameInput).split()) == 6:
        tempHeads, tempRows = searchSQLDatabase.search_for_multiple_names(str(nameInput))
        headers, rows = searchSQLDatabase.search_by_ID_mentors(str(nameInput).split()[-1])
        dictHolder = '['
        for row in rows:
            if str(row[6]) == '0':
                tempLst = list(row)
                tempLst[6] = 'Undergrad'
                row = tuple(tempLst)
            elif str(row[6]) == '1':
                tempLst = list(row)
                tempLst[6] = 'Grad student'
                row = tuple(tempLst)
            elif str(row[6]) == '2':
                tempLst = list(row)
                tempLst[6] = 'Postdoc'
                row = tuple(tempLst)
            elif str(row[6]) == '3':
                tempLst = list(row)
                tempLst[6] = 'Research Scientist'
                row = tuple(tempLst)
            elif str(row[6]) == '4':
                tempLst = list(row)
                tempLst[6] = 'Collaborator'
                row = tuple(tempLst)
            if row[1] is None:
                tempLst = list(row)
                tempLst[1] = ''
                row = tuple(tempLst)
            dictHolder += '{"name": "' + str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + '", "location": "' + str(
                    row[3]) + '", "coords": [' + str(row[4]) + ',' + str(row[5]) + '],"relation": "' + str(
                    row[6]) + '", "years": "' + str(row[7]) + ',' + str(row[8]) + '"},'
        tempRows = tempRows[0]
        if tempRows[1] is None:
            tempLst = list(tempRows)
            tempLst[1] = ''
            tempRows = tuple(tempLst)
        dictHolder += '{"name": "' + str(tempRows[0]) + ' ' + str(tempRows[1]) + ' ' + str(tempRows[2]) + '", "relation": "Current Location", "location": "' + str(
            tempRows[3]) + '", "years": " ", "coords": [' + str(tempRows[5]) + ',' + str(tempRows[6]) + ']},'
        dictHolder = dictHolder[:-1]
        dictHolder += ']'
        print('<html>')
        print('<body>')
        print('<div id = "results_table" class = "tableScroller">')
        print('<html>')
        print('<table id = "cool_table" class = table-fill width="30%">')
        print('<thead>')
        print('<tr>')
        print('<th class ="text-left">Name</th>')
        print('<th class ="text-left">Institution</th>')
        print('<th class ="text-left">Relationship</th>')
        print('</tr>')
        print('</thead>')
        print('<tbody class="table-hover">')
        for row in rows:
            if row[1] is None:
                tempLst = list(row)
                tempLst[1] = ''
                row = tuple(tempLst)
            if str(row[6]) == '0':
                    tempLst = list(row)
                    tempLst[6] = 'Undergrad'
                    row = tuple(tempLst)
            elif str(row[6]) == '1':
                tempLst = list(row)
                tempLst[6] = 'Grad student'
                row = tuple(tempLst)
            elif str(row[6]) == '2':
                tempLst = list(row)
                tempLst[6] = 'Postdoc'
                row = tuple(tempLst)
            elif str(row[6]) == '3':
                tempLst = list(row)
                tempLst[6] = 'Research Scientist'
                row = tuple(tempLst)
            elif str(row[6]) == '4':
                tempLst = list(row)
                tempLst[6] = 'Collaborator'
                row = tuple(tempLst)
            print('<tr>')
            print('<td class="text-left">' + str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + '</td>')
            print('<td class="text-left">' + str(row[3]) + '</td>',)
            print('<td class="text-left">' + str(row[6]) + '</td>',)
            print('</tr>')
        print('<tr>')
        print('<td class="text-left">' + str(tempRows[0]) + ' ' + str(tempRows[1]) + ' ' + str(tempRows[2]) + '</td>')
        print('<td class="text-left">' + str(tempRows[3]) + '</td>',)
        print('<td class="text-left">' + 'Current Location' + '</td>',)
        print('</tr>')
        print('</tbody>')
        print('</table>')
        print(' <p id="mapPointSave" hidden>' + dictHolder + '</p>')
        print('</html>')
        print('</div>')
        print('</body>')
        print('</html>')

    if len(str(nameInput).split()) > 1 & len(str(nameInput).split())<6:
        tempHeads, tempRows = searchSQLDatabase.search_for_multiple_names(str(nameInput))
        checkMultiple = len(tempRows)
        #Go forward as usual if a 3 part name is provide OR if the two part name is unique
        if checkMultiple <= 1:
            headers, rows = searchSQLDatabase.search_by_name_mentors(str(nameInput))
            dictHolder = '['
            for row in rows:
                if str(row[6]) == '0':
                    tempLst = list(row)
                    tempLst[6] = 'Undergrad'
                    row = tuple(tempLst)
                elif str(row[6]) == '1':
                    tempLst = list(row)
                    tempLst[6] = 'Grad student'
                    row = tuple(tempLst)
                elif str(row[6]) == '2':
                    tempLst = list(row)
                    tempLst[6] = 'Postdoc'
                    row = tuple(tempLst)
                elif str(row[6]) == '3':
                    tempLst = list(row)
                    tempLst[6] = 'Research Scientist'
                    row = tuple(tempLst)
                elif str(row[6]) == '4':
                    tempLst = list(row)
                    tempLst[6] = 'Collaborator'
                    row = tuple(tempLst)
                if row[1] is None:
                    tempLst = list(row)
                    tempLst[1] = ''
                    row = tuple(tempLst)
                dictHolder += '{"name": "' + str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + '", "location": "' + str(
                    row[3]) + '", "coords": [' + str(row[4]) + ',' + str(row[5]) + '],"relation": "' + str(
                    row[6]) + '", "years": "' + str(row[7]) + ',' + str(row[8]) + '"},'
        if checkMultiple==1:
            tempRows = tempRows[0]
            tempLst = list(tempRows)
            tempLst[1] = ''
            tempRows = tuple(tempLst)
            dictHolder += '{"name": "' + str(tempRows[0]) + ' ' + str(tempRows[1]) + ' ' + str(tempRows[2]) + '", "relation": "Current Location", "location": "' + \
                          str(tempRows[3]) + '", "years": " ", "coords": [' + str(tempRows[5]) + ',' + str(tempRows[6]) + ']},'
            dictHolder = dictHolder[:-1]
            dictHolder += ']'
            print('<html>')
            print('<body>')
            print('<div id = "results_table" class = "tableScroller">')
            print('<html>')
            print('<table id = "cool_table" class = table-fill width="30%">')
            print('<thead>')
            print('<tr>')
            print('<th class ="text-left">Name</th>')
            print('<th class ="text-left">Institution</th>')
            print('<th class ="text-left">Relationship</th>')
            print('</tr>')
            print('</thead>')
            print('<tbody class="table-hover">')
            for row in rows:
                if row[1] is None:
                    tempLst = list(row)
                    tempLst[1] = ''
                    row = tuple(tempLst)
                if str(row[6]) == '0':
                    tempLst = list(row)
                    tempLst[6] = 'Undergrad'
                    row = tuple(tempLst)
                elif str(row[6]) == '1':
                    tempLst = list(row)
                    tempLst[6] = 'Grad student'
                    row = tuple(tempLst)
                elif str(row[6]) == '2':
                    tempLst = list(row)
                    tempLst[6] = 'Postdoc'
                    row = tuple(tempLst)
                elif str(row[6]) == '3':
                    tempLst = list(row)
                    tempLst[6] = 'Research Scientist'
                    row = tuple(tempLst)
                elif str(row[6]) == '4':
                    tempLst = list(row)
                    tempLst[6] = 'Collaborator'
                    row = tuple(tempLst)
                print('<tr>')
                print('<td class="text-left">' + str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + '</td>')
                print('<td class="text-left">' + str(row[3]) + '</td>', )
                print('<td class="text-left">' + str(row[6]) + '</td>', )
                print('</tr>')
            print('<tr>')
            print(
                '<td class="text-left">' + str(tempRows[0]) + ' ' + str(tempRows[1]) + ' ' + str(tempRows[2]) + '</td>')
            print('<td class="text-left">' + str(tempRows[3]) + '</td>', )
            print('<td class="text-left">' + 'Current Location' + '</td>', )
            print('</tr>')
            print('</tbody>')
            print('</table>')
            print(' <p id="mapPointSave" hidden>' + dictHolder + '</p>')
            print('</html>')
            print('</div>')
            print('</body>')
            print('</html>')

        elif checkMultiple>1:
            dictHolder = '[]'
            print('<html>')
            print('<body>')
            print('<div id="results_table">')
            print('    <select id="choose_name_table" class = "soption" style="width:350px">')
            for row in tempRows:
                if row[1] is None:
                    tempLst = list(row)
                    tempLst[1] = ''
                    row = tuple(tempLst)
                print('    <option value = "THIS IS AN ID NUM ' + str(row[4]) + '">' + str(
                    row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + ' ' + str(row[3]) + ' ' + '</option>',)
            print('    </select><br>')
            print(' <div class="visible">')
            print(' <input type="submit" value="Search" onclick="getNameSelect()"/>')
            print(' </div>')
            print(' <p id="selectOptionSave" hidden>' + str(optionInput) + '</p>')
            print(' <p id="mapPointSave" hidden>' + dictHolder + '</p>')
            print(' </div>')
            print('</body>')
            print('</html>')

    elif len(nameInput.split()) == 1:
        headers, rows = searchSQLDatabase.search_by_last_name(str(nameInput))
        dictHolder = '[]'
        if len(rows)==0:
            print('<html>')
            print('<body>')
            print('<div id="results_table">')
            print('No results found')
        else:
            print('<html>')
            print('<body>')
            print('<div id="results_table">')
            print('    <select id="choose_name_table" class = "soption" style="width:350px">')
            for row in rows:
                    if row[1] is None:
                        tempLst = list(row)
                        tempLst[1] = ''
                        row = tuple(tempLst)

                    print('    <option value = "THIS IS AN ID NUM ' + str(row[4]) + '">' + str(
                        row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + ' ' + str(row[3]) + ' ' + '</option>',)
            print('    </select>')
            print(' <div class="visible"><br>')
            print(' <input type="button" value="Search" onclick="getNameSelect()"/>')
            print(' </div>')
            print(' <p id="selectOptionSave" hidden>' + str(optionInput) + '</p>')
        print(' <p id="mapPointSave" hidden>' + dictHolder + '</p>')
        print(' </div>')
        print('</body>')
        print('</html>')

elif optionInput == "family":

    if not (form.has_key("name")):
        returnError("No name input?")
        sys.exit(0)

    nameInput = form["name"].value
    if len(str(nameInput).split()) == 6:
        # tempHeads, tempRows = searchSQLDatabase.search_for_multiple_names(str(nameInput))
        headers, rows = searchSQLDatabase.search_by_ID_students_cur_locs(str(nameInput).split()[-1])
        dictHolder = '['
        for row in rows:
            if str(row[6]) == '0':
                tempLst = list(row)
                tempLst[6] = 'Undergrad'
                row = tuple(tempLst)
            elif str(row[6]) == '1':
                tempLst = list(row)
                tempLst[6] = 'Grad student'
                row = tuple(tempLst)
            elif str(row[6]) == '2':
                tempLst = list(row)
                tempLst[6] = 'Postdoc'
                row = tuple(tempLst)
            elif str(row[6]) == '3':
                tempLst = list(row)
                tempLst[6] = 'Research Scientist'
                row = tuple(tempLst)
            elif str(row[6]) == '4':
                tempLst = list(row)
                tempLst[6] = 'Collaborator'
                row = tuple(tempLst)
            if row[1] is None:
                tempLst = list(row)
                tempLst[1] = ''
                row = tuple(tempLst)
            dictHolder += '{"name": "' + str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + '", "location": "' + str(
                row[3]) + '", "coords": [' + str(row[4]) + ',' + str(row[5]) + '],"relation": "Current Location, was a ' + str(
                row[6]) + '", "years": "' + str(row[7]) + ',' + str(row[8]) + '"},'

        dictHolder = dictHolder[:-1]
        dictHolder += ']'
        print('<html>')
        print('<body>')
        print('<div id = "results_table" class = "tableScroller">')
        print('<html>')
        print('<table id = "cool_table" class = table-fill width="30%">')
        print('<thead>')
        print('<tr>')
        print('<th class ="text-left">Name</th>')
        print('<th class ="text-left">Institution</th>')
        print('<th class ="text-left">Relationship</th>')
        print('</tr>')
        print('</thead>')
        print('<tbody class="table-hover">')
        for row in rows:
            if row[1] is None:
                tempLst = list(row)
                tempLst[1] = ''
                row = tuple(tempLst)
            if str(row[6]) == '0':
                    tempLst = list(row)
                    tempLst[6] = 'Undergrad'
                    row = tuple(tempLst)
            elif str(row[6]) == '1':
                tempLst = list(row)
                tempLst[6] = 'Grad student'
                row = tuple(tempLst)
            elif str(row[6]) == '2':
                tempLst = list(row)
                tempLst[6] = 'Postdoc'
                row = tuple(tempLst)
            elif str(row[6]) == '3':
                tempLst = list(row)
                tempLst[6] = 'Research Scientist'
                row = tuple(tempLst)
            elif str(row[6]) == '4':
                tempLst = list(row)
                tempLst[6] = 'Collaborator'
                row = tuple(tempLst)
            print('<tr>')
            print('<td class="text-left">' + str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + '</td>')
            print('<td class="text-left">' + str(row[3]) + '</td>', )
            print('<td class="text-left">' + str(row[6]) + '</td>', )
            print('</tr>')
        print('</tbody>')
        print('</table>')
        print(' <p id="mapPointSave" hidden>' + dictHolder + '</p>')
        print('</html>')
        print('</div>')
        print('</body>')
        print('</html>')

    if len(str(nameInput).split()) > 1 & len(str(nameInput).split())<6:
        tempHeads, tempRows = searchSQLDatabase.search_for_multiple_names(str(nameInput))
        checkMultiple = len(tempRows)
        # Go forward as usual if a 3 part name is provided OR if the two part name is unique
        if checkMultiple <= 1:
            headers, rows = searchSQLDatabase.search_by_name_students_curr_locs(str(nameInput))
            dictHolder = '['
            for row in rows:
                if str(row[6]) == '0':
                    tempLst = list(row)
                    tempLst[6] = 'Undergrad'
                    row = tuple(tempLst)
                elif str(row[6]) == '1':
                    tempLst = list(row)
                    tempLst[6] = 'Grad student'
                    row = tuple(tempLst)
                elif str(row[6]) == '2':
                    tempLst = list(row)
                    tempLst[6] = 'Postdoc'
                    row = tuple(tempLst)
                elif str(row[6]) == '3':
                    tempLst = list(row)
                    tempLst[6] = 'Research Scientist'
                    row = tuple(tempLst)
                elif str(row[6]) == '4':
                    tempLst = list(row)
                    tempLst[6] = 'Collaborator'
                    row = tuple(tempLst)
                if row[1] is None:
                    tempLst = list(row)
                    tempLst[1] = ''
                    row = tuple(tempLst)
                dictHolder += '{"name": "' + str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + '", "location": "' + str(
                    row[3]) + '", "coords": [' + str(row[4]) + ',' + str(row[5]) + '],"relation": "Current Location, was a ' + str(
                    row[6]) + '", "years": "' + str(row[7]) + ',' + str(row[8]) + '"},'

            dictHolder = dictHolder[:-1]
            dictHolder += ']'
            print('<html>')
            print('<body>')
            print('<div id = "results_table" class = "tableScroller">')
            print('<html>')
            print('<table id = "cool_table" class = table-fill width="30%">')
            print('<thead>')
            print('<tr>')
            print('<th class ="text-left">Name</th>')
            print('<th class ="text-left">Institution</th>')
            print('<th class ="text-left">Relationship</th>')
            print('</tr>')
            print('</thead>')
            print('<tbody class="table-hover">')
            for row in rows:
                if row[1] is None:
                    tempLst = list(row)
                    tempLst[1] = ''
                    row = tuple(tempLst)
                if str(row[6]) == '0':
                    tempLst = list(row)
                    tempLst[6] = 'Undergrad'
                    row = tuple(tempLst)
                elif str(row[6]) == '1':
                    tempLst = list(row)
                    tempLst[6] = 'Grad student'
                    row = tuple(tempLst)
                elif str(row[6]) == '2':
                    tempLst = list(row)
                    tempLst[6] = 'Postdoc'
                    row = tuple(tempLst)
                elif str(row[6]) == '3':
                    tempLst = list(row)
                    tempLst[6] = 'Research Scientist'
                    row = tuple(tempLst)
                elif str(row[6]) == '4':
                    tempLst = list(row)
                    tempLst[6] = 'Collaborator'
                    row = tuple(tempLst)
                print('<tr>')
                print('<td class="text-left">' + str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + '</td>')
                print('<td class="text-left">' + str(row[3]) + '</td>', )
                print('<td class="text-left">' + str(row[6]) + '</td>', )
                print('</tr>')
            print('</tbody>')
            print('</table>')
            print(' <p id="mapPointSave" hidden>' + dictHolder + '</p>')
            print('</html>')
            print('</div>')
            print('</body>')
            print('</html>')

        elif checkMultiple>1:
            dictHolder = '[]'
            print('<html>')
            print('<body>')
            print('<div id="results_table">')
            print('    <select id="choose_name_table" class = "soption" style="width:350px">')
            for row in tempRows:
                if row[1] is None:
                    tempLst = list(row)
                    tempLst[1] = ''
                    row = tuple(tempLst)
                print('    <option value = "THIS IS AN ID NUM ' + str(row[4]) + '">' + str(
                    row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + ' ' + str(row[3]) + ' ' + '</option>', )
            print('    </select>')
            print(' <div class="visible">')
            print(' <input type="submit" value="Search" onclick="getNameSelect()"/>')
            print(' </div>')
            print(' <p id="selectOptionSave" hidden>' + str(optionInput) + '</p>')
            print(' <p id="mapPointSave" hidden>' + dictHolder + '</p>')
            print(' </div>')
            print('</body>')
            print('</html>')

    elif len(nameInput.split()) == 1:
        headers, rows = searchSQLDatabase.search_by_last_name(str(nameInput))
        dictHolder = '[]'
        print('<html>')
        print('<body>')
        print('<div id="results_table">')
        if len(rows)==0:
            print('No results found')
        else:
            print('    <select id="choose_name_table" class = "soption" style="width:350px">')
            for row in rows:
                    if row[1] is None:
                        tempLst = list(row)
                        tempLst[1] = ''
                        row = tuple(tempLst)
                    print('    <option value = "THIS IS AN ID NUM ' + str(row[4]) + '">' + str(
                        row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + ' ' + str(row[3]) + ' ' + '</option>',)
            print('    </select>')
            print(' <div class="visible">')
            print(' <input type="button" value="Search" onclick="getNameSelect()"/>')
            print(' </div>')
            print(' <p id="selectOptionSave" hidden>' + str(optionInput) + '</p>')
        print(' <p id="mapPointSave" hidden>' + dictHolder + '</p>')
        print(' </div>')
        print('</body>')
        print('</html>')

elif optionInput == "field":

    if not (form.has_key("field")):
        returnError("No field input?")
        sys.exit(0)

    if not (form.has_key("currentInstitution")):
        returnError("No current institution input?")
        sys.exit(0)

    if not (form.has_key("distance")):
        returnError("No distance input?")
        sys.exit(0)

    fieldInput = form["field"].value
    locationInput = form["currentInstitution"].value
    distanceInput = form["distance"].value
    distanceInput = float(distanceInput)
    distanceInputLat = distanceInput/69
    distanceInputLong = distanceInput/55
    headers, rows = searchSQLDatabase.search_by_location_nearby(locationInput,fieldInput,distanceInputLat,distanceInputLong)
    dictHolder = '['
    for row in rows:
        if row[1] is None:
            tempLst = list(row)
            tempLst[1] = ''
            row = tuple(tempLst)
        dictHolder += '{"name": "' + str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + '", "location": "' + str(
            row[3]) + '", "coords": [' + str(row[4]) + ',' + str(row[5]) + '],"relation": "' + str(
            row[6]) + '", "years": ""},'

    dictHolder = dictHolder[:-1]
    dictHolder += ']'
    print('<html>')
    print('<body>')
    print('<div id = "results_table" class = "tableScroller">')
    print('<html>')
    print('<table id = "cool_table" class = table-fill width="30%">')
    print('<thead>')
    print('<tr>')
    print('<th class ="text-left">Name</th>')
    print('<th class ="text-left">Institution</th>')
    print('<th class ="text-left">Relationship</th>')
    print('</tr>')
    print('</thead>')
    print('<tbody class="table-hover">')
    for row in rows:
        if row[1] is None:
            tempLst = list(row)
            tempLst[1] = ''
            row = tuple(tempLst)
        print('<tr>')
        print('<td class="text-left">' + str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + '</td>')
        print('<td class="text-left">' + str(row[3]) + '</td>',)
        print('<td class="text-left">' + str(row[6]) + '</td>',)
        print('</tr>')
    print('</tbody>')
    print('</table>')
    print(' <p id="mapPointSave" hidden>' + dictHolder + '</p>')
    print('</html>')
    print('</div>')
    print('</body>')
    print('</html>')
