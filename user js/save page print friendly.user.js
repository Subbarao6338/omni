// ==UserScript==
// @name         Append All Pages and Print Friendly
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Append all pages of a website into one page, make it print-friendly, and save as MHTML
// @author       You
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
  'use strict';
  var allPages = [];
  var currentPage = 1;
  var totalPages = 0;
  var nextPageLink = document.querySelector('a.next-page, a.next, a.pagination-next');

  // Function to get the total number of pages
  function getTotalPages() {
    // Check if the website uses a pagination system
    var pagination = document.querySelector('div.pagination');
    if (pagination) {
      // Get the total number of pages from the pagination system
      var totalPagesElement = pagination.querySelector('span.total-pages');
      if (totalPagesElement) {
        totalPages = parseInt(totalPagesElement.textContent);
      }
    }
  }

  // Function to append all pages into one page
  function appendAllPages() {
    // Get the total number of pages
    getTotalPages();
    // Loop through all pages and append their content
    for (var i = 1; i <= totalPages; i++) {
      // Get the content of the current page
      var currentPageContent = document.body.innerHTML;
      // Append the content of the current page to the allPages array
      allPages.push(currentPageContent);
      // Go to the next page
      if (i < totalPages) {
        // Check if the next page link uses JavaScript to load the next page
        if (nextPageLink.getAttribute('onclick')) {
          // Simulate a click on the link to load the next page
          nextPageLink.click();
        } else {
          // Go to the next page using the URL
          var nextPageUrl = nextPageLink.href;
          window.location.href = nextPageUrl;
        }
      }
    }
  }

  // Function to make the page print-friendly
  function makePrintFriendly() {
    // Remove unnecessary elements from the page
    var unnecessaryElements = document.querySelectorAll('nav, footer, aside');
    unnecessaryElements.forEach(function(element) {
      element.remove();
    });
    // Simplify the layout and formatting of the page
    var mainContent = document.querySelector('main, article');
    if (mainContent) {
      mainContent.style.width = '100%';
      mainContent.style.margin = '0 auto';
    }
    var paragraphs = document.querySelectorAll('p');
    paragraphs.forEach(function(paragraph) {
      paragraph.style.fontFamily = 'Arial, sans-serif';
      paragraph.style.fontSize = '16px';
      paragraph.style.lineHeight = '1.5';
    });
  }

  // Function to handle pages that use JavaScript to load content
  function handleJavaScriptLoadedContent() {
    // Check if the page uses JavaScript to load content
    var scriptTags = document.querySelectorAll('script');
    scriptTags.forEach(function(scriptTag) {
      if (scriptTag.src) {
        // Load the content using AJAX
        var xhr = new XMLHttpRequest();
        xhr.open('GET', scriptTag.src, true);
        xhr.onload = function() {
          if (xhr.status === 200) {
            var content = xhr.responseText;
            var parser = new DOMParser();
            var doc = parser.parseFromString(content, 'text/html');
            var mainContent = doc.querySelector('main, article');
            if (mainContent) {
              document.body.appendChild(mainContent);
            }
          }
        };
        xhr.send();
      }
    });
  }

  // Function to handle pages that use AJAX or other dynamic loading methods
  function handleAjaxLoadedContent() {
    // Check if the page uses AJAX to load content
    var xhr = new XMLHttpRequest();
    xhr.open('GET', window.location.href, true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        var content = xhr.responseText;
        var parser = new DOMParser();
        var doc = parser.parseFromString(content, 'text/html');
        var mainContent = doc.querySelector('main, article');
        if (mainContent) {
          document.body.appendChild(mainContent);
        }
      }
    };
    xhr.send();
  }

  // Function to handle pages that use anti-scraping measures to prevent automated content loading
  function handleAntiScrapingMeasures() {
    // Check for CAPTCHAs or other challenges
    var captcha = document.querySelector('iframe[src*="captcha"]');
    if (captcha) {
      // Handle CAPTCHA or other challenge
      console.log('CAPTCHA detected. Please handle manually.');
    }
  }

    // Function to save the appended page as MHTML
  function saveAsMHTML() {
    // Create a new MHTML file
    var mhtmlFile = new Blob([allPages.join('')], { type: 'message/rfc822' });
    // Save the MHTML file
    var a = document.createElement('a');
    a.href = URL.createObjectURL(mhtmlFile);
    a.download = 'appended-page.mhtml';
    a.click();
  }

  // Append all pages into one page
  appendAllPages();
  // Make the page print-friendly
  makePrintFriendly();
  // Handle pages that use JavaScript to load content
  handleJavaScriptLoadedContent();
  // Handle pages that use AJAX or other dynamic loading methods
  handleAjaxLoadedContent();
  // Handle pages that use anti-scraping measures to prevent automated content loading
  handleAntiScrapingMeasures();
  // Save the appended page as MHTML
  saveAsMHTML();
})();

// Function to get the total number of pages
function getTotalPages() {
  // Check if the website uses a pagination system
  var pagination = document.querySelector('div.pagination');
  if (pagination) {
    // Get the total number of pages from the pagination system
    var totalPagesElement = pagination.querySelector('span.total-pages');
    if (totalPagesElement) {
      totalPages = parseInt(totalPagesElement.textContent);
    }
  }
}

// Function to append all pages into one page
function appendAllPages() {
  // Get the total number of pages
  getTotalPages();
  // Loop through all pages and append their content
  for (var i = 1; i <= totalPages; i++) {
    // Get the content of the current page
    var currentPageContent = document.body.innerHTML;
    // Append the content of the current page to the allPages array
    allPages.push(currentPageContent);
    // Go to the next page
    if (i < totalPages) {
      // Check if the next page link uses JavaScript to load the next page
      if (nextPageLink.getAttribute('onclick')) {
        // Simulate a click on the link to load the next page
        nextPageLink.click();
      } else {
        // Go to the next page using the URL
        var nextPageUrl = nextPageLink.href;
        window.location.href = nextPageUrl;
      }
    }
  }
}

// Function to make the page print-friendly
function makePrintFriendly() {
  // Remove unnecessary elements from the page
  var unnecessaryElements = document.querySelectorAll('nav, footer, aside');
  unnecessaryElements.forEach(function(element) {
    element.remove();
  });
  // Simplify the layout and formatting of the page
  var mainContent = document.querySelector('main, article');
  if (mainContent) {
    mainContent.style.width = '100%';
    mainContent.style.margin = '0 auto';
  }
  var paragraphs = document.querySelectorAll('p');
  paragraphs.forEach(function(paragraph) {
    paragraph.style.fontFamily = 'Arial, sans-serif';
    paragraph.style.fontSize = '16px';
    paragraph.style.lineHeight = '1.5';
  });
}

// Function to handle pages that use JavaScript to load content
function handleJavaScriptLoadedContent() {
  // Check if the page uses JavaScript to load content
  var scriptTags = document.querySelectorAll('script');
  scriptTags.forEach(function(scriptTag) {
    if (scriptTag.src) {
      // Load the content using AJAX
      var xhr = new XMLHttpRequest();
      xhr.open('GET', scriptTag.src, true);
      xhr.onload = function() {
        if (xhr.status === 200) {
          var content = xhr.responseText;
          var parser = new DOMParser();
          var doc = parser.parseFromString(content, 'text/html');
          var mainContent = doc.querySelector('main, article');
          if (mainContent) {
            document.body.appendChild(mainContent);
          }
        }
      };
      xhr.send();
    }
  });
}

// Function to handle pages that use AJAX or other dynamic loading methods
function handleAjaxLoadedContent() {
  // Check if the page uses AJAX to load content
  var xhr = new XMLHttpRequest();
  xhr.open('GET', window.location.href, true);
  xhr.onload = function() {
    if (xhr.status === 200) {
      var content = xhr.responseText;
      var parser = new DOMParser();
      var doc = parser.parseFromString(content, 'text/html');
      var mainContent = doc.querySelector('main, article');
      if (mainContent) {
        document.body.appendChild(mainContent);
      }
    }
  };
  xhr.send();
}

// Function to handle pages that use anti-scraping measures to prevent automated content loading
function handleAntiScrapingMeasures() {
    // Check for CAPTCHAs or other challenges
  var captcha = document.querySelector('iframe[src*="captcha"]');
  if (captcha) {
    // Handle CAPTCHA or other challenge
    console.log('CAPTCHA detected. Please handle manually.');
  }
}

// Function to save the appended page as MHTML
function saveAsMHTML() {
  // Create a new MHTML file
  var mhtmlFile = new Blob([allPages.join('')], { type: 'message/rfc822' });
  // Save the MHTML file
  var a = document.createElement('a');
  a.href = URL.createObjectURL(mhtmlFile);
  a.download = 'appended-page.mhtml';
  a.click();
}

// Append all pages into one page
appendAllPages();
// Make the page print-friendly
makePrintFriendly();
// Handle pages that use JavaScript to load content
handleJavaScriptLoadedContent();
// Handle pages that use AJAX or other dynamic loading methods
handleAjaxLoadedContent();
// Handle pages that use anti-scraping measures to prevent automated content loading
handleAntiScrapingMeasures();
// Save the appended page as MHTML
saveAsMHTML();


