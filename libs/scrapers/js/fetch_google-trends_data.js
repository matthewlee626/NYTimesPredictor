const XLSX = require('xlsx')
const googleTrends = require('google-trends-api');

function to_json(workbook) {
    var result = {};
    workbook.SheetNames.forEach(function(sheetName) {
        var roa = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
        if(roa.length > 0){
            result[sheetName] = roa;
        }
    });
    return result;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function write(json_raw, isbn) {

	json = JSON.parse(json_raw)

	var container = json['default']['timelineData']

	var ws_data = [['Date', 'GT_SearchIndex']]

	for (var x in container) {
		var temp = []

		var date = container[x]['formattedTime']
		var searchIndex = container[x]['value'][0]
		temp.push(date)
		temp.push(searchIndex)

		ws_data.push(temp)

		//console.log('Date: ' + date + ', Index: ' + searchIndex)
	}

	var ws_name = 'Search Index Values by Date';

	/* make worksheet */
	var ws = XLSX.utils.aoa_to_sheet(ws_data);
	var wb = XLSX.utils.book_new();

	/* Add the worksheet to the workbook */
	XLSX.utils.book_append_sheet(wb, ws, ws_name);
	file_name = isbn.concat('.csv')
	path = 'C:\\Users\\Siddhant\\Desktop\\sera\\nytimes_books\\js\\datadump\\'
	file_location = path.concat(file_name)
	XLSX.writeFile(wb, file_location);

	console.log(file_name + ' has been written.')
}

async function execute() {
	var wb = XLSX.readFile('titleISBNbothdates.csv')
	//var wb = XLSX.readFile('book_info.csv')

	var sheetJSON = to_json(wb)
	var wsJSON = sheetJSON['Sheet1']

	//console.log(wsJSON)

	for (i in wsJSON) {
		//initial variables
		var book = wsJSON[i]
		var title = book['Title'].toString()
		var isbn = (book['ISBN']).toString()

		var first_date_raw = new Date(1900, 0, book['FirstDate'] - 1)
		var last_date_raw = new Date(1900, 0, book['LastDate'] - 1)
		var first_date_yyyymmdd = first_date_raw.toISOString().slice(0,10)
		var last_date_yyyymmdd = last_date_raw.toISOString().slice(0,10)

		console.log(title)
		console.log(isbn)
		//console.log(publish_date)
		console.log('Date first on chart: ' + first_date_yyyymmdd)
		console.log('Date last on chart: ' + last_date_yyyymmdd)

		var days_before = 30 
		var days_after = 30

		//these dates correspond to the beginning and ending lookup dates
		var start_date_raw = new Date(1900, 0, (book['FirstDate'] - days_before) - 1)
		var end_date_raw = new Date(1900, 0, (book['LastDate'] + days_after) - 1)

		var start_date_yyyymmdd = start_date_raw.toISOString().slice(0,10)
		var end_date_yyyymmdd = end_date_raw.toISOString().slice(0,10)

		console.log('Searching start date: ' + start_date_yyyymmdd)
		console.log('Searching end date: ' + end_date_yyyymmdd + '\n\n')

		var u_keyword = (title.toLowerCase()).concat(' book') 
		var u_startTime = new Date(start_date_yyyymmdd)
		var u_endTime =  new Date(end_date_yyyymmdd)
		var u_geo = 'US'

		googleTrends.interestOverTime({keyword: u_keyword, 
				startTime: u_startTime,
				endTime: u_endTime,
				geo: u_geo
			}).then(function(results){
			    //console.log(results)
				json = results

			    //console.log(json)

			    if ( (JSON.parse(json)['default']['timelineData']).length == 0) {
			    	research(title.toLowerCase(), u_startTime, u_endTime, u_geo, isbn)
			    } else {
			    	write(json, isbn)
				}
				// for (var key in json) {
				// 	console.log(json[key]);
				// }
		})
		.catch(function(err){
		  console.error(err);
		});

		await sleep(1000);
	}
}

async function research(u_keyword, u_startTime, u_endTime, u_geo, isbn) {
	googleTrends.interestOverTime({keyword: u_keyword, 
				startTime: u_startTime,
				endTime: u_endTime,
				geo: u_geo
			}).then(function(results){
			    //console.log(results)
				json = results

			    //3console.log(json)

			    write(json, isbn)
				// for (var key in json) {
				// 	console.log(json[key]);
				// }
		})
		.catch(function(err){
		  console.error(err);
		});

		await sleep(1000);
}

execute()
