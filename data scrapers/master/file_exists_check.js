var fs = require('fs') 

isbn = 307265722
if (fs.existsSync('C:\\Users\\Siddhant\\Desktop\\sera\\nytimes_books\\js\\datadump\\' + isbn + '.csv')) { // or fs.existsSync
    console.log('exists')
}