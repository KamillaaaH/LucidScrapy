/*
 * File:   support.h
 * Author: kamilla
 *
 * Created on August 12, 2012, 10:41 PM
 */

#ifndef _hashset_
#define _hashset_

void CreateNewHashPy(int elemSize, int numBuckets);
static int CompareLetter(const void *elem1, const void *elem2);
static int HashFrequency(const void *elem, int numBuckets);
void EnterItemPy(char item);

#endif