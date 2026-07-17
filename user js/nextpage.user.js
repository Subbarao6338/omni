// ==UserScript==
// @name         Next Page Loader
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Load next page content into current page
// @author       You
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
  'use strict';
  var nextPageLink = document.querySelector('a.next-page, a.next, a.pagination-next');
  var nextPageLoaded = false;

  // Function to load next page content
  function loadNextPage() {
    if (nextPageLink) {
      var nextPageUrl = nextPageLink.href;
      // Check if next page link uses JavaScript to load the next page
      if (nextPageLink.getAttribute('onclick')) {
        // Simulate a click on the link to load the next page
        nextPageLink.click();
      } else {
        // Check if next page content is loaded using AJAX or other dynamic loading methods
        var xhr = new XMLHttpRequest();
        xhr.open('GET', nextPageUrl, true);
        xhr.onload = function() {
          if (xhr.status === 200) {
            var nextPageContent = xhr.responseText;
            var parser = new DOMParser();
            var doc = parser.parseFromString(nextPageContent, 'text/html');
            var nextPageHtml = doc.body.innerHTML;
            var currentPageHtml = document.body.innerHTML;
            document.body.innerHTML = currentPageHtml + nextPageHtml;
          }
        };
        xhr.send();
      }
    }
  }

  // Function to check if page uses anti-scraping measures
  function checkAntiScraping() {
    // Check for CAPTCHAs or other challenges
    var captcha = document.querySelector('iframe[src*="captcha"]');
    if (captcha) {
      // Handle CAPTCHA or other challenge
      console.log('CAPTCHA detected. Please handle manually.');
    }
  }

  // Add event listener to window.onscroll event
  window.addEventListener('scroll', function() {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight && !nextPageLoaded) {
      // Check for anti-scraping measures
      checkAntiScraping();
      // Load next page content
      loadNextPage();
      nextPageLoaded = true;
    }
  });
})();
