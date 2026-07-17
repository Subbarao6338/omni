// ==UserScript==
// @name         Print Friendly
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Make pages print-friendly
// @author       You
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
  'use strict';
  var printButton = document.createElement('button');
  printButton.textContent = 'Print';
  printButton.onclick = function() {
    window.print();
  };
  document.body.appendChild(printButton);

  // Function to remove unnecessary elements from the page
  function removeUnnecessaryElements() {
    // Remove ads and other distracting content
    var ads = document.querySelectorAll('iframe[src*="ads"], div[class*="ad"]');
    ads.forEach(function(ad) {
      ad.remove();
    });
    // Remove other unnecessary elements
    var unnecessaryElements = document.querySelectorAll('nav, footer, aside');
    unnecessaryElements.forEach(function(element) {
      element.remove();
    });
  }

  // Function to simplify the layout and formatting of the page
  function simplifyLayout() {
    // Simplify the layout
    var mainContent = document.querySelector('main, article');
    if (mainContent) {
      mainContent.style.width = '100%';
      mainContent.style.margin = '0 auto';
    }
    // Simplify the formatting
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

  // Remove unnecessary elements from the page
  removeUnnecessaryElements();
  // Simplify the layout and formatting of the page
  simplifyLayout();
  // Handle pages that use JavaScript to load content
  handleJavaScriptLoadedContent();
  // Handle pages that use AJAX or other dynamic loading methods
  handleAjaxLoadedContent();
  // Handle pages that use anti-scraping measures to prevent automated content loading
  handleAntiScrapingMeasures();
})();
