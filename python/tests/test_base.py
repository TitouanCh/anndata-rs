from anndata_rs import AnnData, AnnDataSet, read

import math
import numpy as np
import pandas as pd
import pytest
from pathlib import Path
import uuid
from scipy import sparse as sp
from scipy.sparse import csr_matrix, issparse, random
from hypothesis import given, example, settings, HealthCheck, strategies as st
from hypothesis.extra.numpy import *

def h5ad(dir=Path("./")):
    dir.mkdir(exist_ok=True)
    return str(dir / Path(str(uuid.uuid4()) + ".h5ad"))

@given(x=arrays(
    integer_dtypes(endianness='=') | floating_dtypes(endianness='=', sizes=(32, 64)) |
    unsigned_integer_dtypes(endianness = '='),
    array_shapes(min_dims=2, max_dims=2, min_side=0, max_side=5),
))
@example(x=np.array([], dtype=np.int8))
@settings(suppress_health_check = [HealthCheck.function_scoped_fixture])
def test_assign_arrays(x, tmp_path):
    adata = AnnData(filename = h5ad(tmp_path))
    adata.uns['x'] = x
    x_ = adata.uns['x']
    np.testing.assert_array_equal(x_, x)

@given(x=st.floats())
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_assign_floats(x, tmp_path):
    adata = AnnData(filename = h5ad(tmp_path))
    adata.uns['x'] = x
    x_ = adata.uns['x']
    assert (x_ == x or (math.isnan(x) and math.isnan(x_)))

def test_creation(tmp_path):
    # some test objects that we use below
    adata_dense = AnnData(filename = h5ad(tmp_path), X = np.array([[1, 2], [3, 4]]))
    file = adata_dense.filename
    adata_dense.close()
    adata_dense = read(file, mode="r+")
    adata_dense.uns['x'] = 0.2

    adata_sparse = AnnData(
        filename = h5ad(tmp_path),
        X = csr_matrix([[0, 2, 3], [0, 5, 6]]),
        obs = dict(obs_names=["s1", "s2"], anno1=["c1", "c2"]),
        var = dict(var_names=["a", "b", "c"]),
    )

    adata = AnnData(filename=h5ad(tmp_path))
    assert adata.n_obs == 0
    adata.obsm =dict(X_pca=np.array([[1, 2], [3, 4]]))
    assert adata.n_obs == 2

    AnnData(X = np.array([[1, 2], [3, 4]]), filename=h5ad(tmp_path))
    AnnData(X = np.array([[1, 2], [3, 4]]), obsm = {}, filename=h5ad(tmp_path))
    #AnnData(X = sp.eye(2), filename="data.h5ad")
    X = np.array([[1, 2, 3], [4, 5, 6]])
    adata = AnnData(
        X=X,
        obs=dict(Obs=["A", "B"]),
        var=dict(Feat=["a", "b", "c"]),
        obsm=dict(X_pca=np.array([[1, 2], [3, 4]])),
        filename=h5ad(tmp_path),
    )

    adata.var["Count"] = [1,2,3]
    assert list(adata.var["Count"]) == [1,2,3]
    '''
    with pytest.raises(ValueError):
        AnnData(X = np.array([[1, 2], [3, 4]]), obsm = dict(TooLong=[1, 2, 3, 4]))
    '''

    # init with empty data matrix
    #shape = (3, 5)
    #adata = AnnData(None, uns=dict(test=np.array((3, 3))), shape=shape)
    #assert adata.X is None
    #assert adata.shape == shape
    #assert "test" in adata.uns

def test_type(tmp_path):
    adata = AnnData(filename = h5ad(tmp_path), X = np.array([[1, 2], [3, 4]]))

    dtypes = [
        "int8", "int16", "int32", "int64",
        "uint8", "uint16", "uint32", "uint64",
        "float32", "float64", "bool",
    ]

    for ty in dtypes:
        x = random(20, 5, 0.9, format="csr", dtype = ty)
        adata.uns[ty] = x
        assert (adata.uns[ty] != x).nnz == 0

    """
    for ty in dtypes:
        x = getattr(np, ty)(10)
        adata.uns[ty] = x
        assert adata.uns[ty] == x
    """

    x = "test"
    adata.uns["str"] = x
    assert adata.uns["str"] == x

    x = {
        "a": 1,
        "b": 2.0,
        "c": {"1": 2, "2": 5},
        "d": "test",
    }
    adata.uns["dict"] = x
    assert adata.uns["dict"] == x