/*
 * File:   hashset.c
 * Author: kamilla
 *
 * Created on August 12, 2012, 5:33 PM
 */

#include "hashset.h"
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>



/**
 * Function:  HashSetNew
 * ---------------------
 **/
void HashSetNew(hashset *h, int elemSize, int numBuckets,
		HashSetHashFunction hashfn, HashSetCompareFunction comparefn, HashSetFreeFunction freefn)
{

/** An assert is raised unless all of the following conditions are met:
	*    - elemSize is greater than 0.
	*    - numBuckets is greater than 0.
	*    - hashfn is non-NULL
	*    - comparefn is non-NULL
	**/
	assert(h != NULL);
	assert(elemSize > 0);
	assert(numBuckets > 0);
	assert(hashfn != NULL);
	assert(comparefn != NULL);
	//initialization of vector;
	vector v;
	//now v->initialAllocation will be equal of numBuckets
	VectorNew(&v, elemSize, (VectorFreeFunction)freefn, numBuckets);

	//initialization of hash
	h->v = v;
	h->hashFunction = hashfn;
	h->compareFunction = comparefn;

	//initialization of vector
        int i = 0;
	for(i = 0; i <= numBuckets; i++)
	{
		void *initValues = calloc(i, h->v.elemSize);
		VectorAppend(&h->v, initValues);
	}
}

/**
 * Function: HashSetDispose
 * ------------------------
 * Disposes of any resources acquired during the lifetime of the
 * hashset.
	*/
void HashSetDispose(hashset *h)
{
	assert(h != NULL);
	//cleaning vector
	VectorDispose(&h->v);

}

/**
 * Function: HashSetCount
 * ----------------------
 * Returns the number of elements residing in
 * the specified hashset.
 */
int HashSetCount(const hashset *h)
{
	/** An assert is raised if hashset is null
	*/
	assert(h != NULL);
	//using VectorLength to return the number of elems
	return VectorLength(&h->v);
}


void HashSetMap(hashset *h, HashSetMapFunction mapfn, void *auxData)
{
	/** An assert is raised if hashset is null
	*/
	assert(h != NULL);
	//sending mapfn to VectorMap
	VectorMap(&h->v, (VectorMapFunction) mapfn, auxData);
}

/**
 * Function: HashSetEnter
 * ----------------------
 * Inserts the specified element into the specified
 * hashset.
 */
void HashSetEnter(hashset *h, const void *elemAddr)
{
	assert(h != NULL);
	assert(elemAddr != NULL);

	//Using the hashFunction to calculate the hash of the element
	int elem = h->hashFunction(elemAddr, h->v.initialAllocation);

	/* An assert is raised if the specified address is NULL, or
   * if the embedded hash function somehow computes a hash code
   * for the element that is out of the [0, numBuckets) range.
   */
	assert(-1<elem && elem<h->v.initialAllocation);

	//Replacing the value in the specified address
	VectorReplace(&h->v, elemAddr, elem);
}

/**
 * Function: HashSetLookup
 * -----------------------
 * Examines the specified hashset to see if anything matches
 * the item residing at the specified elemAddr.  If a match
 * is found, then the address of the stored item is returned.
 * If no match is found, then NULL is returned as a sentinel.
 */
void *HashSetLookup(const hashset *h, const void *elemAddr)
{
	assert(h != NULL);
	assert(elemAddr != NULL);

	//Using the hashFunction to calculate the hash of the element
	int hashElem = h->hashFunction(elemAddr, h->v.initialAllocation);

	/* An assert is raised if the specified address is NULL, or
   * if the embedded hash function somehow computes a hash code
   * for the element that is out of the [0, numBuckets) range.
   */
	assert(-1<hashElem && hashElem<h->v.initialAllocation);

	//search the position of elem
	void *position = VectorNth(&h->v, hashElem);

	/** Understand that the key (residing at elemAddr) only needs
 	 * to match a stored element as far as the hash and compare
   * functions are concerned.
  **/

	//((char*)match - (char*)v->elems)/v->elemSize;
	//int matchAddr = (((char*)position - (char*)h->v.elems)/h->v.elemSize);
 	//if(matchAddr)
		//return matchAddr;

	return NULL;
}



