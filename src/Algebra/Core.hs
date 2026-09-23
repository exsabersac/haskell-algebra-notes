{-# LANGUAGE DeriveFunctor #-}
-- | 手写的 Fix / Free / 函子积木与 fold。
-- 对应文档：docs/初始代数/定义.md、docs/Free/Fix编码.md、docs/函子组合/常见组合.md
module Algebra.Core
  ( Fix(..)
  , cata
  , Free(..)
  , foldFree
  , interpret
  , Const(..)
  , Sum(..)
  , Product(..)
  , Compose(..)
  , Identity(..)
  ) where

-- | μF 的载体编码。见 docs/初始代数/定义.md
newtype Fix f = Fix { unFix :: f (Fix f) }

-- | 初始代数的唯一同态：cata φ ∘ in = φ ∘ F(cata φ)
cata :: Functor f => (f a -> a) -> Fix f -> a
cata phi = phi . fmap (cata phi) . unFix

-- | Free f a ≅ μY. (a + f Y)。Pure = 外部生成元。见 docs/Free/生成元.md
data Free f a
  = Pure a
  | Free (f (Free f a))
  deriving Functor

-- | foldFree = cata for (a + f(-))，且 onPure = id。见 docs/Free/foldFree与cata.md
foldFree :: Functor f => (f a -> a) -> Free f a -> a
foldFree _   (Pure x) = x
foldFree phi (Free t) = phi (fmap (foldFree phi) t)

-- | 更一般：先解释生成元，再按 f-代数折。
interpret :: Functor f => (a -> b) -> (f b -> b) -> Free f a -> b
interpret onPure onFree = go
  where
    go (Pure x) = onPure x
    go (Free t) = onFree (fmap go t)

-- | 常对象：叶子 / 标签，不递归。
newtype Const a r = Const a
  deriving (Show)

instance Functor (Const a) where
  fmap _ (Const x) = Const x

-- | 和：二选一。
data Sum f g r = InL (f r) | InR (g r)
  deriving (Show)

instance (Functor f, Functor g) => Functor (Sum f g) where
  fmap h (InL fr) = InL (fmap h fr)
  fmap h (InR gr) = InR (fmap h gr)

-- | 积：同时要两边。
data Product f g r = Product (f r) (g r)
  deriving (Show)

instance (Functor f, Functor g) => Functor (Product f g) where
  fmap h (Product fr gr) = Product (fmap h fr) (fmap h gr)

-- | 复合：外层 f 里再嵌 g。
newtype Compose f g r = Compose (f (g r))
  deriving (Show)

instance (Functor f, Functor g) => Functor (Compose f g) where
  fmap h (Compose fgr) = Compose (fmap (fmap h) fgr)

newtype Identity a = Identity { runIdentity :: a }
  deriving (Functor, Show)
