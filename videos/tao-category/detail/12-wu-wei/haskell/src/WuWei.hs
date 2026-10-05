{-# LANGUAGE RankNTypes #-}
-- | 进阶深讲第 12 集「无为而无不为」：米田引理；Speak/CPS；Kan 扩张。
--   参考：DaoFP 第2章（identity = wu wei）、第9章 The Yoneda Lemma、
--         第20章 Kan Extensions（Right Kan extension in Haskell）；
--         CTFP 2.5 The Yoneda Lemma, 2.6 Yoneda Embedding, 3.11 Kan Extensions
--   （按 CTFP 惯例在 Hask 中忽略 ⊥）
module WuWei
  ( Yoneda (..)
  , toYoneda
  , fromYoneda
  , Speak
  , hear
  , redeem
  , Ran (..)
  , yonedaToRan
  , ranToYoneda
  ) where

import Data.Functor.Identity (Identity (..))

-- {{snip:s_yoneda}}
-- 米田：Nat(Hom(a,−), f) ≅ f a
-- Yoneda f a 收集「对一切 x，用 a→x 产出 f x」
newtype Yoneda f a = Yoneda { runYoneda :: forall x. (a -> x) -> f x }

toYoneda :: Functor f => f a -> Yoneda f a
toYoneda fa = Yoneda (\h -> fmap h fa)    -- 无不为：用 fmap 应对任何箭头

fromYoneda :: Yoneda f a -> f a
fromYoneda (Yoneda g) = g id              -- 无为：只给它 id
-- {{/snip}}

instance Functor (Yoneda f) where
  fmap h (Yoneda g) = Yoneda (\k -> g (k . h))   -- fmap 只做函数复合

-- {{snip:s_redeem}}
-- 回到第七集：f = Identity
-- (forall x. (a -> x) -> x)  ≅  a
type Speak a = forall x. (a -> x) -> x

hear :: a -> Speak a
hear a = \k -> k a

redeem :: Speak a -> a
redeem s = s id
-- {{/snip}}

-- {{snip:s_ran}}
-- 右 Kan 扩张：Ran_p f a = ∀b. (a → p b) → f b
-- 特例 p = Identity ⇒ Yoneda f ≅ Ran Identity f
newtype Ran g h a = Ran { runRan :: forall b. (a -> g b) -> h b }

yonedaToRan :: Yoneda f a -> Ran Identity f a
yonedaToRan (Yoneda g) = Ran (\k -> g (runIdentity . k))

ranToYoneda :: Ran Identity f a -> Yoneda f a
ranToYoneda (Ran r) = Yoneda (\k -> r (Identity . k))
-- {{/snip}}
