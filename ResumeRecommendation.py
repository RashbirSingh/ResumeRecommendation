#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 11:49:27 2019

@author: ubuntu
"""

import pandas as pd
import numpy as np
import fitz

class ResumePointCalculator:
    
    def __init__(self, resumeLocation):
        self.resume = fitz.open(resumeLocation)
      
    """Gets and prints the spreadsheet's header columns
    
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
        
    """Gets and prints the spreadsheet's header columns
    
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
        
    """Gets and prints the spreadsheet's header columns
    
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
        links = []
        for pagenumber in range(self.resume.pageCount):
            page = self.resume[pagenumber]
            for linkdict in range(len(page.getLinks())):
                links.append(page.getLinks()[linkdict]['uri'])
        return list(set(links))
    
    def resumeToText(self, outputType):
        resumeData = []
        for pagenumber in range(self.resume.pageCount):
            page = self.resume[pagenumber]
            resumeData.append(page.getText(outputType))
        return resumeData
        
        
        