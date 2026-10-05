{-# LANGUAGE RankNTypes #-}
-- | 第六段「无为而无不为」：米田引理；恒等函子情形即 CPS；Kan 扩张。
--   参考：DaoFP 第2章（identity = wu wei）、第9章 The Yoneda Lemma、第20章 Kan Extensions；
--         CTFP 2.5, 2.6, 3.11
module Seg6Yoneda where

import Data.Functor.Identity (Identity (..))
import Seg1Dao (Speak, hear)

-- {{snip:s6a}}
newtype Yoneda f a = Yoneda (forall x. (a -> x) -> f x)

toYoneda :: Functor f => f a -> Yoneda f a
toYoneda fa = Yoneda (\h -> fmap h fa)    -- 无不为

fromYoneda :: Yoneda f a -> f a
fromYoneda (Yoneda g) = g id              -- 无为：只给它 id
-- {{/snip}}

instance Functor (Yoneda f) where
  fmap h (Yoneda g) = Yoneda (\k -> g (k . h))   -- fmap 只做函数复合

-- {{snip:s6b}}
-- 回到第一句：f = Identity
-- (forall x. (a -> x) -> x)  ≅  a
redeem :: Speak a -> a
redeem s = s id

-- 所有概念都是 Kan 扩张：Yoneda f ≅ Ran Identity f
newtype Ran g h a = Ran (forall b. (a -> g b) -> h b)
-- {{/snip}}

yonedaToRan :: Yoneda f a -> Ran Identity f a
yonedaToRan (Yoneda g) = Ran (\k -> g (runIdentity . k))

ranToYoneda :: Ran Identity f a -> Yoneda f a
ranToYoneda (Ran r) = Yoneda (\k -> r (Identity . k))

-- | redeem 与 hear 互逆
roundTrip :: a -> a
roundTrip a = redeem (hear a)
