# easySearch line bot
> This is simple line api based bot using QANet-SQUAD-1.
> The base for chatbot replying are the articles fetched from a travel website.
> Due to privacy and policy of the travel website, the data canot be shared without permission so you can fetch your own, > The sample code is given below (Under Extracting data source)

[![npm][namee here ]][url here]


![easysearch](header.png)

## Installation

OS X & Linux:

```sh

```

Windows:

```sh

```

## Usage example

A few motivating and useful examples of how your product can be used. 

## Development setup

Install all development dependencies, check by using 
> pip freeze > requirements.txt
## Other requirements 
>  Download pre-trained wiki-news-300d-1M-subword.magnitude (remeber to use pymagnitude format) 
>  
## Release History

* 1.0.0
    * CHANGE: Updated basic implementation (module code remains unchanged)

## Extracting data source 
* for this you can use this image screenshot as the reference
![Screenshot](images/fetch.jpg)

## Article search 
* In order to make good use of data, I did a word-vector to article-vector conversion.
* This is done by TF-IDF weighted mean for all words in an article. (Except stopword, I
* use the stopwords list from nltk)
![Screenshot](images/article search.jpg)


## Meta

Your Name – [@tatheerhussain](https://twitter.com/tatheerhussain) 



## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request



<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics

