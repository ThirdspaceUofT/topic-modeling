{
 "metadata": {
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.3-final"
  },
  "orig_nbformat": 2,
  "kernelspec": {
   "name": "Python 3.8.3 64-bit ('ProgramData': virtualenv)",
   "display_name": "Python 3.8.3 64-bit ('ProgramData': virtualenv)",
   "metadata": {
    "interpreter": {
     "hash": "b3ba2566441a7c06988d0923437866b63cedc61552a5af99d1f4fb67d367b25f"
    }
   }
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2,
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 43,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import os\n",
    "import preprocessor as p\n",
    "import string"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [
    {
     "output_type": "stream",
     "name": "stdout",
     "text": [
      "Collecting tweet-preprocessor\n  Using cached tweet_preprocessor-0.6.0-py3-none-any.whl (27 kB)\nInstalling collected packages: tweet-preprocessor\nSuccessfully installed tweet-preprocessor-0.6.0\n"
     ]
    }
   ],
   "source": [
    "# !pip install tweet-preprocessor"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "metadata": {},
   "outputs": [],
   "source": [
    "from nltk.tokenize import TweetTokenizer\n",
    "from emoji import demojize\n",
    "import re\n",
    "\n",
    "tokenizer = TweetTokenizer()\n",
    "\n",
    "def normalizeToken(token):\n",
    "    lowercased_token = token.lower()\n",
    "    if token.startswith(\"@\"):\n",
    "        return \" \"\n",
    "    elif token.startswith(\"#\"):\n",
    "        return \" \"\n",
    "    elif lowercased_token.startswith(\"http\") or lowercased_token.startswith(\"www\"):\n",
    "        return \" \"\n",
    "    elif len(token) == 1:\n",
    "        return demojize(token)\n",
    "    else:\n",
    "        if token == \"’\":\n",
    "            return \"'\"\n",
    "        elif token == \"…\":\n",
    "            return \"...\"\n",
    "        else:\n",
    "            return token\n",
    "\n",
    "def normalizeTweet(tweet):\n",
    "\n",
    "    normTweet = tweet.replace(\"cannot \", \" \").replace(\"n't \", \" \").replace(\"n 't \", \" \").replace(\"ca n't\", \" \").replace(\"ai n't\", \" \")\n",
    "    normTweet = normTweet.replace(\"'m \", \" 'm \").replace(\"'re \", \" 're \").replace(\"'s \", \" 's \").replace(\" i'll \", \" \").replace(\"'d \", \" 'd \").replace(\"'ve \", \" 've \")\n",
    "    normTweet = normTweet.replace(\" p . m .\", \"  p.m.\") .replace(\" p . m \", \" p.m \").replace(\" a . m .\", \" a.m.\").replace(\" a . m \", \" a.m \")\n",
    "    normTweet = normTweet.replace(\"RT \", \"\").replace(\"rt \", \"\")\n",
    "    \n",
    "    normTweet = normTweet.translate((str.maketrans('','',string.punctuation)))\n",
    "\n",
    "    tokens = tokenizer.tokenize(normTweet.replace(\"’\", \"\").replace(\"…\", \" \"))\n",
    "    tokens = [word for word in tokens if len(word)>1]\n",
    "    tokens = [x for x in tokens if not (x.isdigit() \n",
    "                                         or x[0] == '-' and x[1:].isdigit())]\n",
    "\n",
    "    normTweet = \" \".join([normalizeToken(token) for token in tokens])\n",
    "    \n",
    "    # normTweet = re.sub(r\",([0-9]{2,4}) , ([0-9]{2,4})\", r\",\\1,\\2\", normTweet)\n",
    "    # normTweet = re.sub(r\"([0-9]{1,3}) / ([0-9]{2,4})\", r\"\\1/\\2\", normTweet)\n",
    "    # normTweet = re.sub(r\"([0-9]{1,3})- ([0-9]{2,4})\", r\"\\1-\\2\", normTweet)\n",
    "    \n",
    "    return \" \".join(normTweet.split())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 61,
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "def generate_texts(mon):\n",
    "    directory = mon+'/'\n",
    "    output_dir = 'refined/'+directory\n",
    "    \n",
    "    for filename in os.listdir(directory):\n",
    "        if(filename.endswith('.csv')):\n",
    "            if(mon == 'Jul' or mon == 'Jun'):\n",
    "                df = pd.read_csv(directory+filename, encoding='utf-8', usecols = [1, 3], header = None)\n",
    "                df = df[df[3] == 'en']\n",
    "                del df[3]\n",
    "            else:\n",
    "                df = pd.read_csv(directory+filename, encoding='utf-8', usecols = [1, 4], header = None)\n",
    "                df = df[df[4] == 'en']\n",
    "                del df[4]\n",
    "            df[1] = [normalizeTweet(item) for item in df[1]]\n",
    "            df.drop_duplicates(subset =[1], keep = False, inplace = True) \n",
    "            with open(output_dir+filename[:-4]+'.txt', 'w', encoding='utf-8') as f:\n",
    "                for item in df[1]:\n",
    "                    f.write(\"%s\\n\" % item)\n",
    "            # return 0\n",
    "    return 0\n",
    "\n",
    "months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']\n",
    "\n",
    "for mon in months:\n",
    "    df = generate_texts(mon)\n",
    "    directory = mon+'/'\n",
    "    \n",
    "    with open(mon+'_files.txt', 'w', encoding='utf-8') as f:\n",
    "        for filename in os.listdir(directory):\n",
    "            if(filename.endswith('.csv')):\n",
    "                f.write(\"%s.txt\\n\" % filename[:-4])\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ]
}