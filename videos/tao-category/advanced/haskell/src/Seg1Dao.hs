{-# LANGUAGE RankNTypes #-}
-- | 第一段「道可道，非常道」：对象不可道，只有箭头可道。
--   参考：DaoFP 第1章 Clean Slate；第3章 Isomorphism（"At the arrows look!"）
module Seg1Dao
  ( Dao        -- 只导出类型，不导出构造子：内部不可见
  , birth
  , speak
  , Speak
  , hear
  ) where

-- {{snip:s1}}
-- 不可道：构造子不导出，外界看不见内部
newtype Dao = Dao Integer

birth :: Integer -> Dao        -- 射入 Dao 的箭头
birth = Dao

speak :: Dao -> String         -- 射出 Dao 的箭头
speak (Dao n) = "道" ++ show n

-- 可道者：从 a 出发的一切说法
type Speak a = forall x. (a -> x) -> x
-- {{/snip}}

-- | 把一个值变成“它的全部说法”（第六段会证明这是同构）
hear :: a -> Speak a
hear a k = k a
