{-# LANGUAGE RankNTypes #-}
-- | 进阶深讲第 7 集「道可道」：对象不可道，箭头可道；Speak / hear 作米田铺垫。
--   参考：DaoFP 第1章 Clean Slate；第3章 Isomorphism（"At the arrows look!"）
--         CTFP 1.1, 1.2
module DaoSayable
  ( Dao        -- 只导出类型，不导出构造子：内部不可见
  , birth
  , speak
  , Speak
  , hear
  , demoSpeak
  , demoHear
  ) where

-- {{snip:s_dao}}
-- 不可道：构造子不导出，外界看不见内部
newtype Dao = Dao Integer

birth :: Integer -> Dao        -- 射入 Dao 的箭头
birth = Dao

speak :: Dao -> String         -- 射出 Dao 的箭头
speak (Dao n) = "道" ++ show n
-- {{/snip}}

-- {{snip:s_speak}}
-- 可道者：从 a 出发的一切说法（续体风格）
type Speak a = forall x. (a -> x) -> x
-- {{/snip}}

-- {{snip:s_hear}}
-- 把一个值收成「它的全部说法」（米田侧的最小种子）
hear :: a -> Speak a
hear a k = k a
-- {{/snip}}

-- {{snip:s_demo}}
-- 演示：边界上的箭头；说法喂给下一步
demoSpeak :: String
demoSpeak = speak (birth 42)           -- "道42"

demoHear :: Int
demoHear = hear (42 :: Int) (+ 1)      -- 43
-- {{/snip}}
