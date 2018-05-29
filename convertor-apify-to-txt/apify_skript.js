//http://www.imdb.com/title/tt[\d{7}]/[.*]

function pageFunction(context) {
    // called on every page the crawler visits, use it to extract data from it
    var $ = context.jQuery;
    
    if (context.request.label === "PAGE") {
        context.skipLinks();
    
        var ratings = [];
        var texts = [];
        
        $('span.rating-other-user-rating > span:not([class])').each( function() {
            ratings.push($(this).text());    
        });
        $('div.review-container > div.lister-item-content > div.content > div.text.show-more__control').each( function() {
            texts.push($(this).text());    
        });
    
        var result = {
            rating: ratings,
            text: texts
        };
        return result;
        }
        
    else if (context.request.label === "DETAIL") {
         //context.enqueuePage(request);
         context.skipOutput();
    } else { 
    context.skipOutput();
    }
}