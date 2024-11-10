macro_rules! dyn_match {
    ($scalar:expr, $enum:ident, $inner_macro:ident) => {
        match $scalar {
            $enum::I8 => $inner_macro!(i8),
            $enum::I16 => $inner_macro!(i16),
            $enum::I32 => $inner_macro!(i32),
            $enum::I64 => $inner_macro!(i64),
            $enum::U8 => $inner_macro!(u8),
            $enum::U16 => $inner_macro!(u16),
            $enum::U32 => $inner_macro!(u32),
            $enum::U64 => $inner_macro!(u64),
            $enum::F32 => $inner_macro!(f32),
            $enum::F64 => $inner_macro!(f64),
            $enum::Bool => $inner_macro!(bool),
            $enum::String => $inner_macro!(String),
        }
    };
}

macro_rules! dyn_map {
    ($scalar:expr, $enum:ident, $inner_macro:ident) => {
        match $scalar {
            $enum::I8(_val) => $inner_macro!(I8, _val),
            $enum::I16(_val) => $inner_macro!(I16, _val),
            $enum::I32(_val) => $inner_macro!(I32, _val),
            $enum::I64(_val) => $inner_macro!(I64, _val),
            $enum::U8(_val) => $inner_macro!(U8, _val),
            $enum::U16(_val) => $inner_macro!(U16, _val),
            $enum::U32(_val) => $inner_macro!(U32, _val),
            $enum::U64(_val) => $inner_macro!(U64, _val),
            $enum::F32(_val) => $inner_macro!(F32, _val),
            $enum::F64(_val) => $inner_macro!(F64, _val),
            $enum::Bool(_val) => $inner_macro!(Bool, _val),
            $enum::String(_val) => $inner_macro!(String, _val),
        }
    };
}

macro_rules! dyn_map_fun {
    ($scalar:expr, $enum:ident, $fun:ident $(, $arg:expr)*) => {
        match $scalar {
            $enum::I8(_val) => _val.$fun($($arg),*),
            $enum::I16(_val) => _val.$fun($($arg),*),
            $enum::I32(_val) => _val.$fun($($arg),*),
            $enum::I64(_val) => _val.$fun($($arg),*),
            $enum::U8(_val) => _val.$fun($($arg),*),
            $enum::U16(_val) => _val.$fun($($arg),*),
            $enum::U32(_val) => _val.$fun($($arg),*),
            $enum::U64(_val) => _val.$fun($($arg),*),
            $enum::F32(_val) => _val.$fun($($arg),*),
            $enum::F64(_val) => _val.$fun($($arg),*),
            $enum::Bool(_val) => _val.$fun($($arg),*),
            $enum::String(_val) => _val.$fun($($arg),*),
        }
    };
}

pub(crate) use {dyn_match, dyn_map, dyn_map_fun};