#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 11:49:27 2019

@author: ubuntu
"""

import pandas as pd
import numpy as np
import re
import fitz

class ResumePointCalculator:
    
    def __init__(self, resumeLocation):
        self.resume = fitz.open(resumeLocation)
      
    """Opened resume object using fitz and return the opened file
    
    Parameters
    ----------
    None
    
    Returns
    -------
    resumeObject : fitz.Document object
        Opened resume object using fitz
    """
    def docOpen(self):
        resumeObject = fitz.open(self.resumeLocation)
        return resumeObject
        
    """Gives information about pdf
    
    Parameters
    ----------
    resume : fitz.Document object
    
    Returns
    -------
    dict
        Dictionary having
            PageCount : int
                Number of pages in resume
            MetaData : dict
                Resume metadata
            HaveIndex: bool
                Have index(True) or not(False)
            HaveImages: List
                List of bool with page, if page have image(True) or not(False)
    """
    def pdfInfo(self):
        imageList = {}
        for page in range(self.resume.pageCount):
            image = self.resume.getPageImageList(page)
            if len(image) > 0:
                imageList[page] = True
            else:
                imageList[page] = False
        return {"PageCount":self.resume.pageCount,
                "MetaData": self.resume.metadata,
                "HaveIndex":True if len(self.resume.getToC()) > 0 else False,
                "HaveImages": imageList
                }
        
    """Gives links in the pdf if have attached hyperlinks
    
    Parameters
    ----------
    resume : fitz.Document object
        Opened resume object using fitz
    
    Returns
    -------
    list
        List of links inside the resume
    """
    def getLinksList(self):
        #TODO: improve regex based hyperlink detection
        links = []
        urls =[]
        for pagenumber in range(self.resume.pageCount):
            page = self.resume[pagenumber]
            for linkdict in range(len(page.getLinks())):
                links.append(page.getLinks()[linkdict]['uri'])
        resumeData = self.resumeToText()
        for page in range(len(resumeData)):
            urls = re.findall("[localhost|http|https|ftp|file]+://[\w\S(\.|:|/)]+", 
                              resumeData[page])
            for linkOnPage in urls:
                links.append(linkOnPage)
        return list(set(links))
    
    """Reads the resume and gives list per page in text format
    
    Parameters
    ----------
    outputType : (default) Text
        "text": (default) plain text with line breaks. No formatting, no text position details, no images.
        "html": creates a full visual version of the page including any images. 
                This can be displayed with your internet browser.
        "dict": same information level as HTML, but provided as a Python dictionary. 
                See TextPage.extractDICT() for details of its structure.
        "rawdict": a super-set of TextPage.extractDICT(). 
                It additionally provides character detail information like XML. See TextPage.extractRAWDICT() for details of its structure.
        "xhtml": text information level as the TEXT version but includes images. 
                Can also be displayed by internet browsers.
        "xml": contains no images, but full position and font information down to each single text character. 
                Use an XML module to interpret.

    
    Returns
    -------
    list
        List of text inside the resume with size equals number of pages.
    """
    
    def resumeToText(self, outputType="text"):
        resumeData = []
        for pagenumber in range(self.resume.pageCount):
            page = self.resume[pagenumber]
            resumeData.append(page.getText(outputType))
        return resumeData
        
        
        