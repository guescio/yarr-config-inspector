#!/usr/bin/env python3

#******************************************
#This is a tool to inspect YARR configuration and mask files.

#******************************************
__author__ = "Francesco Guescini"
__version__ = "0.0.0"

#******************************************
#import stuff
import streamlit as st
import json
import numpy as np
import matplotlib.pyplot as plt

#******************************************
#page setup
#NOTE this must be the first streamlit command to be run
st.set_page_config(
    page_title = "YARR config inspector",
    #page_icon = "",
    layout = "wide",
    initial_sidebar_state = "expanded")

#container for output text and errors
container = st.container()

#******************************************
#YARR config file inspection
def main():

    #------------------------------------------
    #title
    st.sidebar.title("YARR config inspector")
    #st.sidebar.write("An interface to inspect YARR config and mask files.")

    #------------------------------------------
    #upload config file
    uploaded_file = st.sidebar.file_uploader(
        "Upload a YARR configuration or mask file.",
        type=["json", "before", "after"],
        accept_multiple_files=False,
        key=None,
        help="Upload a YARR configuration or mask file.")

    #------------------------------------------
    #load data from the configuration file
    if uploaded_file is not None:
        
        try:
            data = json.load(uploaded_file)
        except:
            container.error("could not open file")
            return

        #------------------------------------------
        #config file or mask file?
        try:
            key = list(data.keys())[0]
        except:
            container.error("there was a problem reading the input file")
            return

        if key == "Data":
            inspectMask(data)
        elif "RD53" in key:
            inspectConfig(data)

    return
            
#******************************************
#inspect config file
def inspectConfig(data):

    #------------------------------------------
    #RD53A or RD53B?
    chip_type = list(data.keys())[0]

    if "Name" in list(data[chip_type]["Parameter"].keys()):
        name = data[chip_type]["Parameter"]["Name"]
    else:
        name = ""
    container.text(f"name: {name}")

    #get the number of rows and columns
    ncol = len(data[chip_type]["PixelConfig"])
    nrow = len(data[chip_type]["PixelConfig"][0]["Enable"])
    #container.text(f"size: {nrow} rows * {ncol} columns")

    container.text(f"type: {chip_type} ({nrow} rows * {ncol} columns)")

    #------------------------------------------
    #load config data into matrix
    e = np.zeros((nrow, ncol), dtype=int) #Enable
    t = np.zeros((nrow, ncol), dtype=int) #TDAC
    
    #loop over columns
    for jj in range(ncol):
            
        #load column data
        e[:, jj] = data[chip_type]["PixelConfig"][jj]["Enable"]
        t[:, jj] = data[chip_type]["PixelConfig"][jj]["TDAC"]
        
    #------------------------------------------
    #count enabled pixels
    enabled = np.count_nonzero(e)
    container.text(f"pixels enabled: {enabled} / {ncol*nrow} = {100.*enabled/ncol/nrow:.3f}%")
        
    #------------------------------------------
    #print disabled pixels coordinates
    if False:
        disabled_rows, disabled_columns = np.where(e == 0)
        container.text(f"disabled pixels: {list(zip(disabled_columns, disabled_rows))}")
    
    #------------------------------------------
    #draw map of enabled pixels
    if True:
        fig1, ax1 = plt.subplots()
        im1 = ax1.matshow(e)
        ax1.invert_yaxis() #y-axis zero at the bottom
        ax1.xaxis.tick_bottom() #x-axis ticks at the bottom
        ax1.set_ylabel("rows")
        ax1.set_xlabel("columns")
        ax1.set_title("pixel mask")
        cbar1 = plt.colorbar(im1, ticks = [0, 1])#, values = [1, 0])
        cbar1.set_ticklabels([f"disabled\n({(ncol*nrow)-enabled})", f"enabled\n({enabled})"])
        ax1.text(1.0, 1.0, name,
            fontsize="small",
            horizontalalignment="right",
            verticalalignment="bottom",
            transform = ax1.transAxes)

        st.pyplot(fig1)

    #------------------------------------------
    #draw map of pixel TDAC
    if True:
        fig2, ax2 = plt.subplots()
        im2 = ax2.matshow(t)
        ax2.invert_yaxis() #y-axis zero at the bottom
        ax2.xaxis.tick_bottom() #x-axis ticks at the bottom
        ax2.set_ylabel("rows")
        ax2.set_xlabel("columns")
        ax2.set_title("pixel TDAC")
        cbar2 = plt.colorbar(im2)
        cbar2.set_label("TDAC")
        ax2.text(1.0, 1.0, name,
            fontsize="small",
            horizontalalignment="right",
            verticalalignment="bottom",
            transform = ax2.transAxes)

        st.pyplot(fig2)

    #------------------------------------------
    #draw pixel TDAC histogram
    if True:
        fig3, ax3 = plt.subplots()
        n, bins, patches = ax3.hist(t.flatten(), bins=30)
        ax3.set_ylabel("pixels")
        ax3.set_xlabel("TDAC")
        ax3.set_title("pixel TDAC")
        ax3.text(1.0, 1.0, name,
            fontsize="small",
            horizontalalignment="right",
            verticalalignment="bottom",
            transform = ax3.transAxes)

        st.pyplot(fig3)

    return

#******************************************
#inspect mask file
def inspectMask(data):

    #------------------------------------------
    #load config data into matrix
    scan = data["Name"]
    container.text(f"scan: {scan}")
    e = np.array(data["Data"]).T
    nrow, ncol = np.shape(e)
    container.text(f"size: {nrow} rows * {ncol} columns")

    #------------------------------------------
    #count enabled pixels
    enabled = np.count_nonzero(e)
    container.text(f"{enabled} / {ncol*nrow} pixels enabled: {100.*enabled/ncol/nrow:.3f}%")

    #------------------------------------------
    #draw map of enabled pixels from config file
    if True:

        fig, ax = plt.subplots()
        im = ax.matshow(e)
        ax.invert_yaxis() #y-axis zero at the bottom
        ax.xaxis.tick_bottom() #x-axis ticks at the bottom
        ax.set_ylabel("rows")
        ax.set_xlabel("columns")
        ax.set_title("pixel mask")
        cbar = plt.colorbar(im, ticks = [0, 1])#, values = [1, 0])
        cbar.ax.set_yticklabels([f"disabled\n({(ncol*nrow)-enabled})", f"enabled\n({enabled})"])

        st.pyplot(fig)

    return

#******************************************
if __name__ == "__main__":

    #start the YARR file inspection
    main()
