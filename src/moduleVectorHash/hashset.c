/*
 * File:   hashset.c
 * Author: kamilla e maylon
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
        HashSetCompareFunction comparefn, HashSetFreeFunction freefn) {
    /** An assert is raised unless all of the following conditions are met:
     *    - elemSize is greater than 0.
     *    - numBuckets is greater than 0.
     *    - hashfn is non-NULL
     *    - comparefn is non-NULL
     **/
    assert(h != NULL);
    assert(elemSize > 0);
    assert(numBuckets > 0);
    assert(comparefn != NULL);
    //initialization of vector;
    vector v;
    //now v->initialAllocation will be equal of numBuckets
    VectorNew(&v, elemSize, (VectorFreeFunction) freefn, numBuckets);

    //initialization of hash
    h->v = v;
    h->compareFunction = comparefn;
    h->_free = freefn;

    //initialization of vector
    int i = 0;
    for (i = 0; i <= numBuckets; i++) {
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
void HashSetDispose(hashset *h) {
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
int HashSetCount(const hashset *h) {
    /** An assert is raised if hashset is null
     */
    assert(h != NULL);
    //using VectorLength to return the number of elems
    return VectorLength(&h->v);
}

void HashSetMap(hashset *h, HashSetMapFunction mapfn, void *auxData) {
    /** An assert is raised if hashset is null
     */
    assert(h != NULL);
    assert(mapfn !=NULL);
    //sending mapfn to VectorMap
    VectorMap(&h->v, (VectorMapFunction) mapfn, auxData);
}

/**
 * Function: HashSetEnter
 * ----------------------
 * Inserts the specified element into the specified
 * hashset.
 */
void HashSetEnter(hashset *h, const void *elemAddr, int position) {
    //printf("%s", elemAddr);
    
    assert(h != NULL);
    assert(elemAddr != NULL);

    /* An assert is raised if the specified address is NULL, or
     * if the embedded hash function somehow computes a hash code
     * for the element that is out of the [0, numBuckets) range.
     */
    assert(-1 < position && position < h->v.initialAllocation);

    //Replacing the value in the specified address
    VectorReplace(&h->v, elemAddr, position);
}



